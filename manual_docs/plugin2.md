# hardhat-toolbox-viem
This toolbox includes a set of plugins to build Hardhat projects with viem as the connection library and the Node.js test runner for TypeScript tests. It's our recommended toolbox for new Hardhat projects.

# Sample project
You can initialize a project based on this toolbox by running npx hardhat --init and selecting A TypeScript Hardhat project using Node Test Runner and Viem as the project type.

# Manual installation
If you want to add the toolbox manually, first install the package:

```
npm install --save-dev @nomicfoundation/hardhat-toolbox-viem
```
Then add it to your Hardhat configuration:

```
import hardhatToolboxViem from "@nomicfoundation/hardhat-toolbox-viem";

export default {
  plugins: [hardhatToolboxViem],
};
```
# Included functionality
With this toolbox, you can:

Use viem as the connection library for interacting with the network
Write Solidity tests using Hardhat's built-in test runner
Write TypeScript tests using the Node.js test runner and our viem assertions plugin.
Verify contracts with hardhat-verify
Deploy contracts using Hardhat Ignition
# Bundled plugins
When you install @nomicfoundation/hardhat-toolbox-viem, these plugins are automatically installed as peer dependencies:
```
@nomicfoundation/hardhat-ignition
@nomicfoundation/hardhat-ignition-viem
@nomicfoundation/hardhat-keystore
@nomicfoundation/hardhat-network-helpers
@nomicfoundation/hardhat-node-test-runner
@nomicfoundation/hardhat-viem
@nomicfoundation/hardhat-viem-assertions
@nomicfoundation/hardhat-verify
```
# Explicitly installing plugins
In some cases, you may need to manually install one of the included plugins. This can happen if:

You want to use a different version than the one included in the toolbox.
You need to import something from the plugin in your code and need to have it in your package.json to avoid issues.
For example, the @nomicfoundation/hardhat-viem-assertions plugin includes an anyValue predicate that can be used along with the .emitWithArgs assertion. If you want to use this predicate in your code, you need to install the plugin explicitly:


npm install --save-dev @nomicfoundation/hardhat-viem-assertions
Then you'll be able to import things from the plugin:

```
import { anyValue } from "@nomicfoundation/hardhat-viem-assertions/predicates";
```