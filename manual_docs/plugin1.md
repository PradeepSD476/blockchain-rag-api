# hardhat-toolbox-mocha-ethers
This toolbox includes a set of plugins to build Hardhat projects with ethers.js as the connection library and Mocha for TypeScript tests. If you are migrating a Hardhat 2 project that uses that stack, this toolbox is the recommended way to upgrade.

# Sample project
You can initialize a project based on this toolbox by running npx hardhat --init and selecting A TypeScript Hardhat project using Mocha and Ethers.js as the project type.

# Manual installation
If you want to add the toolbox manually, first install the package:

```
npm install --save-dev @nomicfoundation/hardhat-toolbox-mocha-ethers
```
Then add it to your Hardhat configuration:

```
import hardhatToolboxMochaEthers from "@nomicfoundation/hardhat-toolbox-mocha-ethers";

export default {
  plugins: [hardhatToolboxMochaEthers],
};
```
# Included functionality
With this toolbox, you can:

Use ethers.js as the connection library for interacting with the network
Write Solidity tests using Hardhat's built-in test runner
Write TypeScript tests using Mocha and our chai matchers plugin.
Verify contracts with hardhat-verify
Deploy contracts using Hardhat Ignition
# Bundled plugins
When you install @nomicfoundation/hardhat-toolbox-mocha-ethers, these plugins are automatically installed as peer dependencies:
```
@nomicfoundation/hardhat-ethers
@nomicfoundation/hardhat-ethers-chai-matchers
@nomicfoundation/hardhat-ignition
@nomicfoundation/hardhat-ignition-ethers
@nomicfoundation/hardhat-keystore
@nomicfoundation/hardhat-mocha
@nomicfoundation/hardhat-network-helpers
@nomicfoundation/hardhat-typechain
@nomicfoundation/hardhat-verify
@nomicfoundation/ignition-core
```
# Explicitly installing plugins
In some cases, you may need to manually install one of the included plugins. This can happen if:

You want to use a different version than the one included in the toolbox.
You need to import something from the plugin in your code and need to have it in your package.json to avoid issues.
For example, the @nomicfoundation/hardhat-ethers-chai-matchers plugin includes an anyValue predicate that can be used along with the .withArgs matcher. If you want to use this predicate in your code, you need to install the plugin explicitly:

```
npm install --save-dev @nomicfoundation/hardhat-ethers-chai-matchers
```
Then you'll be able to import things from the plugin:

```
import { anyValue } from "@nomicfoundation/hardhat-ethers-chai-matchers/withArgs";
```