# Migrate from Hardhat 2
```
TIP

Hardhat 3 is production-ready and you can migrate today! We'll keep it in beta status as we work on missing features and stabilize it in the near future.
```

# Overview
Hardhat 3 is a complete rewrite of Hardhat 2. While many features are familiar, several fundamental changes mean the new version is not compatible with Hardhat 2 projects out of the box:

ESM-first: Your Hardhat config must be an ES module. Scripts and JavaScript/TypeScript tests can still be CommonJS, but ESM is the default.
Declarative config: Plugins, tasks, and other extensions are configured explicitly in your config instead of being registered by side effects.
Explicit network connections: You create and manage network connections yourself, allowing multiple concurrent connections in one process, but meaning that hre.network no longer represents a single network connection that is immediately available.
Extensibility through hooks: Features like extendConfig and subtask overriding were replaced by the new hooks system. Adding new fields to the Hardhat Runtime Environment with extendEnvironment is no longer possible, but the typical use cases for extending it can be covered by other mechanisms.
Because these changes are significant, this guide recommends starting with a clean config and migrating features step by step, rather than trying to adapt an Hardhat 2 project in place.

# Before starting the migration
Before making any changes, prepare your project so that installing and running Hardhat 3 won't conflict with leftover dependencies, configs, or build artifacts from Hardhat 2.

Check node.js version

Make sure you are using Node.js v22.10.0 or later:

```
node --version
```
Clear caches and artifacts

Run the clean task to avoid issues with stale artifacts or caches:
```
npx hardhat clean
```
Remove Hardhat 2 dependencies

Start by removing these packages from your package.json:
hardhat
Any packages starting with hardhat-, @nomicfoundation/, or @nomiclabs/
solidity-coverage
Then reinstall and check for remaining packages that depend on Hardhat:
```
npm install && npm ls hardhat
```
Repeat until no Hardhat-related dependencies remain.

Rename your old config

Keep your old config for reference, but rename it so you can create a new one alongside it:

```
mv hardhat.config.js hardhat.config.old.js
```
Make your project ESM

Run the following command to set the correct type field in your package.json:
```
npm pkg set type=module
```
(Optional) Adapt your tsconfig.json

If you have a tsconfig.json file, make sure that compilerOptions.module is set to an ESM-compatible value like "esnext".

# Setting up Hardhat 3
With your npm project ready, you can start setting up Hardhat 3.
```
Install Hardhat 3
```

Run the following command to install Hardhat 3:
```
npm install --save-dev hardhat
```
Create an empty config file

Create a hardhat.config.ts file with the following content:

```
import type { HardhatUserConfig } from "hardhat/config";

const config: HardhatUserConfig = {};

export default config;
```
Run the help command

Verify that Hardhat 3 is working by running the help command:
```
npx hardhat --help
```
# Progresively migrating your config
With a minimal version of Hardhat 3 working, you can migrate your config bit by bit.

Let's start with the minimal settings required to compile your contracts.

Add a solidity entry

Copy the solidity entry from your old config as-is. The format is backwards-compatible in Hardhat 3, so it should just work:

```
const config: HardhatUserConfig = {
  solidity: {
    /* your solidity config */
  },
};
```
Compile your contracts

Run the build task to verify that your config is working:
```
npx hardhat build
```
To learn more about the updated config format, and continue with your migration, please take a look at this section.

# Migrating tests
This section assumes that your Hardhat 2 project uses Mocha as its tests runner, which is the default experience.

Install the recommended toolbox for Mocha and Ethers.js

Install the plugin:
```
npm install --save-dev @nomicfoundation/hardhat-toolbox-mocha-ethers
```
Then in your Hardhat config, import the plugin and add it to the list of plugins:

```
import type { HardhatUserConfig } from "hardhat/config";
import hardhatToolboxMochaEthers from "@nomicfoundation/hardhat-toolbox-mocha-ethers";

const config: HardhatUserConfig = {
  plugins: [hardhatToolboxMochaEthers],
  solidity: {
    /* your solidity config */
  },
};
```
Notice that, unlike Hardhat 2, it's not enough to just import the plugin in the config. You also have to add it to the list of plugins.

Update your test files

This is usually the most involved part of the migration, and so it has its own page with the details.

You can start by migrating a single test and run it individually to verify that it works as expected:
```
npx hardhat test test/some-test.ts
```
# Migrating extendConfig and extendEnvironment
These extensibility points were replaced by the hook system. We'll add details on how to migrate them soon.
