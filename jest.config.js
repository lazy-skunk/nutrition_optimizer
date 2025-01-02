/** @type {import('ts-jest').JestConfigWithTsJest} **/
export const testEnvironment = "jsdom";
export const transform = {
  "^.+.tsx?$": ["ts-jest", { isolatedModules: true }],
};
export const preset = "ts-jest";
export const moduleFileExtensions = ["ts", "tsx", "js", "json", "node"];
