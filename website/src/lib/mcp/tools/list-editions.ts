import { defineTool } from "@lovable.dev/mcp-js";
import { z } from "zod";
import { editions } from "../editions";

export default defineTool({
  name: "list_editions",
  title: "List Porn Blocker editions",
  description:
    "Return every Porn Blocker 3.6 edition available for download, including title, tag, description, and download URL.",
  inputSchema: {},
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: () => ({
    content: [
      {
        type: "text",
        text: JSON.stringify(editions, null, 2),
      },
    ],
    structuredContent: { editions },
  }),
});

// Silence unused-import for z in case future edits need it.
void z;
