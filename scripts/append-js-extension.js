import { readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

const JS_OUTPUT_DIR = "./static/js";
const JS_EXTENSION = ".js";
const IMPORT_REGEX = /from\s+["']([^"']+)["']/g;

function appendJsExtension(filePath) {
  const content = readFileSync(filePath, "utf8");

  const updatedContent = content.replace(
    IMPORT_REGEX,
    (originalLine, originalImportPath) => {
      if (originalImportPath.endsWith(JS_EXTENSION)) {
        return originalLine;
      }
      const importPathWithExtension = `from "${originalImportPath}${JS_EXTENSION}"`;
      return importPathWithExtension;
    }
  );

  writeFileSync(filePath, updatedContent, "utf8");
}

function processDirectoryRecursively(directory) {
  const items = readdirSync(directory);

  items.forEach((item) => {
    const fullPath = join(directory, item);

    if (statSync(fullPath).isDirectory()) {
      processDirectoryRecursively(fullPath);
    } else if (item.endsWith(JS_EXTENSION)) {
      appendJsExtension(fullPath);
    }
  });
}

processDirectoryRecursively(JS_OUTPUT_DIR);
