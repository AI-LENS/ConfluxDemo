# Integrating MCP servers
Model Context Protocol (MCP) is a powerful tool to connect your ai agents with any external tools or services. In this guide we will setup a couple of MCP servers easily and integrate them with **Conflux** to build a powerful agent.

> **Note:** There are various different ways to install mcp servers in your system. Even some online services are available that enables you to run mcp servers without installing them in your system. In this guide to keep it simple, we will leverage the **Docker** containers to install multiple mcp servers in your system.

> To get started, you need to have **Docker Desktop** installed in your system. You can follow the official guide for [mac](https://docs.docker.com/desktop/setup/install/mac-install/), [windows](https://docs.docker.com/desktop/setup/install/windows-install/) or [linux](https://docs.docker.com/desktop/setup/install/linux/) to install docker in your system.

## 1. Install MCP Proxy
After installing docker, we need to pull docker image for mcp proxy. This will give us a docker container that can easily setup multiple mcp servers in your system. To do this, run the following command in your terminal:

```bash
docker pull ghcr.io/tbxark/mcp-proxy:latest
```
> If the above command fails, you can try running one of the commands listed in their [GitHub repository](https://github.com/TBXark/mcp-proxy/pkgs/container/mcp-proxy) under `OS/Arch` tab.

## 2. Setup MCP servers
Now that we have the mcp proxy docker image, we can run it to setup multiple mcp servers.
First, we will start by creating a `mcp` folder inside our project directory. (`my-project` in our case)
```bash
mkdir mcp
```
Here we will create a `config.json` file that will contain the configuration for our mcp servers. You can create this file using the following command:

#### Linux/Mac
```bash
touch mcp/config.json
```

#### Windows
```bash
echo "" > mcp/config.json
```
Or you can simply create a new file using your favorite text editor.
Now, open the `config.json` file and copy the following code into it:
```json
{
  "mcpProxy": {
    "baseURL": "http://localhost:9090",
    "addr": ":9090",
    "name": "MCP Proxy",
    "version": "1.0.0",
    "options": {
      "panicIfInvalid": false,
      "logEnabled": true
    }
  },
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "options": {
        "panicIfInvalid": true,
        "logEnabled": false
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "yahoo-finance": {
      "command": "uvx",
      "args": ["mcp-yahoo-finance"]
    }
  }
}
```

Next, cd into the `mcp` folder and run the following command to start the mcp proxy server:
#### Linux/Mac
```bash
$ cd mcp
$ docker run --rm -p 9090:9090 -v $(pwd):/config ghcr.io/tbxark/mcp-proxy:latest
```
#### Windows
```bash
> cd mcp
> docker run --rm -p 9090:9090 -v ${pwd}:/config ghcr.io/tbxark/mcp-proxy:latest
```

You should see mcp-proxy server running and different MCP servers getting connected to it. At the end it will say `All clients initialized`.