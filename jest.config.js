/** @type {import('ts-jest').JestConfigWithTsJest} **/
module.exports = {
  testEnvironment: "jsdom",
  transform: {
    "^.+.tsx?$": ["ts-jest", { isolatedModules: true }],
  },
  preset: "ts-jest",
  moduleFileExtensions: ["ts", "tsx", "js", "json", "node"],
};
