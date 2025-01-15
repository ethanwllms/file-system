import { WebSocketServer } from 'ws';
import fs from "fs/promises";
import path from "path";
import os from 'os';
import { z } from "zod";

const HOST = process.env.HOST || '0.0.0.0'; 
const PORT = process.env.PORT || 8765;


// Command line argument parsing
const args = process.argv.slice(2);
if (args.length === 0) {
    console.error("Usage: node index.js <allowed-directory> [additional-directories...]");
    process.exit(1);
}

// Normalize all paths consistently
function normalizePath(p) {
    return path.normalize(p).toLowerCase();
}

function expandHome(filepath) {
    if (filepath.startsWith('~/') || filepath === '~') {
        return path.join(os.homedir(), filepath.slice(1));
    }
    return filepath;
}

// Store allowed directories in normalized form
const allowedDirectories = args.map(dir => normalizePath(path.resolve(expandHome(dir))));

// Validate that all directories exist and are accessible
await Promise.all(args.map(async (dir) => {
    try {
        const stats = await fs.stat(dir);
        if (!stats.isDirectory()) {
            console.error(`Error: ${dir} is not a directory`);
            process.exit(1);
        }
    }
    catch (error) {
        console.error(`Error accessing directory ${dir}:`, error);
        process.exit(1);
    }
}));

// directory utilities
async function validateAndCreateDirectory(requestedPath, allowedDirectories) {
    const absolutePath = path.resolve(requestedPath);
    
    // You should add additional validation here
    const isAllowed = allowedDirectories.some((dir) => absolutePath.startsWith(dir));
    if (!isAllowed) {
        throw new Error(`Access denied - path outside allowed directories: ${absolutePath}`);
    }

    try {
        await fs.mkdir(absolutePath, { recursive: true });
        return `Successfully created directory at ${requestedPath}`;
    } catch (error) {
        throw new Error(`Failed to create directory: ${error.message}`);
    }
}

// Example integration into WebSocket handler
async function handleCreateDirectory(params, allowedDirectories) {
    console.log('Made it to creation function..')
    console.log(params);
    if (!params || typeof params === 'undefined') {
        throw new Error("Invalid parameters");
    }

    const message = await validateAndCreateDirectory(params, allowedDirectories);
    return { content: [{ type: "text", text: message }] };
}


// Security utilities
async function validatePath(requestedPath) {
    console.log(requestedPath);
    const expandedPath = expandHome(requestedPath);
    const absolute = path.isAbsolute(expandedPath)
        ? path.resolve(expandedPath)
        : path.resolve(process.cwd(), expandedPath);
    const normalizedRequested = normalizePath(absolute);
    
    const isAllowed = allowedDirectories.some(dir => normalizedRequested.startsWith(dir));
    if (!isAllowed) {
        throw new Error(`Access denied - path outside allowed directories: ${absolute}`);
    }
    
    try {
        const realPath = await fs.realpath(absolute);
        const normalizedReal = normalizePath(realPath);
        const isRealPathAllowed = allowedDirectories.some(dir => normalizedReal.startsWith(dir));
        if (!isRealPathAllowed) {
            throw new Error("Access denied - symlink target outside allowed directories");
        }
        return realPath;
    }
    catch (error) {
        const parentDir = path.dirname(absolute);
        try {
            const realParentPath = await fs.realpath(parentDir);
            const normalizedParent = normalizePath(realParentPath);
            const isParentAllowed = allowedDirectories.some(dir => normalizedParent.startsWith(dir));
            if (!isParentAllowed) {
                throw new Error("Access denied - parent directory outside allowed directories");
            }
            return absolute;
        }
        catch {
            throw new Error(`Parent directory does not exist: ${parentDir}`);
        }
    }
}

// File operations utilities
async function getFileStats(filePath) {
    const stats = await fs.stat(filePath);
    return {
        size: stats.size,
        created: stats.birthtime,
        modified: stats.mtime,
        accessed: stats.atime,
        isDirectory: stats.isDirectory(),
        isFile: stats.isFile(),
        permissions: stats.mode.toString(8).slice(-3),
    };
}

async function searchFiles(rootPath, pattern) {
    const results = [];
    async function search(currentPath) {
        const entries = await fs.readdir(currentPath, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            try {
                await validatePath(fullPath);
                if (entry.name.toLowerCase().includes(pattern.toLowerCase())) {
                    results.push(fullPath);
                }
                if (entry.isDirectory()) {
                    await search(fullPath);
                }
            }
            catch (error) {
                continue;
            }
        }
    }
    await search(rootPath);
    return results;
}

// Create WebSocket server
const wss = new WebSocketServer({ host: HOST, port: PORT });

// Handle incoming connections
wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', async (data) => {
        try {
            const message = JSON.parse(data);
            const { method, params, id } = message;
            console.log(message);

            let response = {
                jsonrpc: "2.0",
                id: id
            };

            try {
                switch (method) {
                    case "list_tools":
                        response.result = {
                            tools: [
                                {
                                    name: "read_file",
                                    description: "Read file contents"
                                },
                                {
                                    name: "write_file",
                                    description: "Write to file"
                                },
                                {
                                    name: "list_directory",
                                    description: "List directory contents"
                                },
                                {
                                    name: "search_files",
                                    description: "Search for files"
                                },
                                {
                                    name: "create_directory",
                                    description: "Create new directory"
                                }
                            ]
                        };
                        break;

                    case "call_tool":
                        console.log('Called the tool...');
                        const { name, arguments: args } = params;
                        console.log(args.path);
                        switch (name) {
                            case "read_file": {
                                const validPath = await validatePath(args.path);
                                console.log(validPath);
                                const content = await fs.readFile(validPath, "utf-8");
                                response.result = {
                                    content: [{ type: "text", text: content }]
                                };
                                break;
                            }
                            case "write_file": {
                                const validPath = await validatePath(args.path);
                                await fs.writeFile(validPath, args.content, "utf-8");
                                response.result = {
                                    content: [{ type: "text", text: `Successfully wrote to ${args.path}` }]
                                };
                                break;
                            }
                            case "list_directory": {
                                console.log('listing...');
                                const validPath = await validatePath(args.path);
                                const entries = await fs.readdir(validPath, { withFileTypes: true });
                                const formatted = entries
                                    .map((entry) => `${entry.isDirectory() ? "[DIR]" : "[FILE]"} ${entry.name}`)
                                    .join("\n");
                                response.result = {
                                    content: [{ type: "text", text: formatted }]
                                };
                                console.log(response.result);
                                break;
                            }
                            case "search_files": {
                                const validPath = await validatePath(args.path);
                                const results = await searchFiles(validPath, args.pattern);
                                response.result = {
                                    content: [{ type: "text", text: results.length > 0 ? results.join("\n") : "No matches found" }]
                                };
                                break;
                            }
                            case "create_directory": {
                                console.log('Made it to dir creation..')
                                const newPathResult = await handleCreateDirectory(args.path, allowedDirectories);
                                console.log(newPathResult); // Log the whole result to see the structure
                                const { content } = newPathResult;
                                const successMessage = content.length > 0 ? content[0].text : "Directory creation result is empty";

                                response.result = {
                                    content: [{ type: "text", text: successMessage }]
                                };
                                console.log(response.result);
                                break;
                            };
                            default:
                                throw new Error(`Unknown tool: ${name}`);
                        }
                        break;

                    default:
                        throw new Error(`Unknown method: ${method}`);
                }
            } catch (error) {
                response.error = {
                    code: -32000,
                    message: error.message
                };
            }

            ws.send(JSON.stringify(response));
        } catch (error) {
            console.error('Error processing message:', error);
            ws.send(JSON.stringify({
                jsonrpc: "2.0",
                error: {
                    code: -32700,
                    message: "Parse error"
                },
                id: null
            }));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });

    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
    });
});

console.log(`WebSocket server running on ${HOST}:${PORT}`);
console.log("Allowed directories:", allowedDirectories);
