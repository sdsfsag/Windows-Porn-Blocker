import { defineMcp } from "@lovable.dev/mcp-js";
import listEditions from "./tools/list-editions";

export default defineMcp({
  name: "porn-blocker-mcp",
  title: "Porn Blocker 3.6 MCP",
  version: "0.1.0",
  instructions:
    "Public catalog for Porn Blocker 3.6 — the final release. Use list_editions to enumerate every edition (DE/EN, Lite, Preview, Debian, Turbo) with its download URL.",
  tools: [listEditions],
});
