// Entry program for the make.fun bounty gta6-meme-x-01 ("Post a GTA 6 meme on X").
//
// The entry itself is an X post: a GTA 6 meme picturing make.fun's ghost,
// posted from a public account with make.fun (or @makefunai) and the
// entrant's play code in its text. This program does the one mechanical job
// the grader needs: it carries the post's address from POST.json at the
// repository root into the output directory, as /output/POST.json.
//
// It runs on Node 22 with the standard library only. It reads no network,
// no clock and no file outside the repository, so two runs write the same
// bytes. Local check:
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// After that, out/POST.json is byte for byte the repository's POST.json.
// POST.json starts life holding a placeholder address: replace it with the
// real post address (https://x.com/<handle>/status/<id>) once the meme is
// posted, before submitting.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

let postJson;
try {
  postJson = readFileSync(source, "utf8");
} catch (error) {
  console.error(`could not read ${source}: ${(error as Error).message}`);
  process.exit(1);
}

// The address must be a JSON object naming an X post; refuse anything else
// rather than handing the gate a broken file.
let parsed: unknown;
try {
  parsed = JSON.parse(postJson);
} catch {
  console.error(`POST.json is not valid JSON: ${source}`);
  process.exit(1);
}
if (
  typeof parsed !== "object" ||
  parsed === null ||
  Array.isArray(parsed) ||
  typeof (parsed as { url?: unknown }).url !== "string"
) {
  console.error(`POST.json must be an object like {"url": "https://x.com/..."}: ${source}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
try {
  writeFileSync(target, postJson);
} catch (error) {
  console.error(`could not write ${target}: ${(error as Error).message}`);
  process.exit(1);
}
