# JavaScript/Node.js Samples - Module 02: Getting Started

This directory contains JavaScript/Node.js samples for getting started with Azure AI Foundry using the Azure AI SDK.

## Prerequisites

- Node.js 18.0 or later
- npm or yarn package manager
- Azure AI Foundry project with appropriate permissions
- VS Code or preferred JavaScript IDE

## Quick Start

### 1. Setup Development Environment

```bash
# Verify Node.js installation
node --version
npm --version

# Clone and navigate to JavaScript samples
cd Samples/Module02-Getting-Started/JavaScript
```

### 2. Configure Environment

Create a `.env` file in each sample directory:

```bash
AZURE_AI_FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 3. Install Dependencies

Each sample includes a `package.json` file with required dependencies:

```bash
# Navigate to specific sample directory
cd azure-ai-foundry-setup

# Install packages
npm install

# Run sample
npm start
```

## Available Samples

### 1. azure-ai-foundry-setup
**Purpose**: Demonstrates Azure AI Foundry setup and authentication patterns
**Key Features**:
- Multiple authentication methods
- Configuration management
- Connection validation
- Environment setup

### 2. first-chat-completion
**Purpose**: Basic chat completion application
**Key Features**:
- Interactive chat interface
- Model interaction
- Response handling
- Conversation management

### 3. error-handling
**Purpose**: Robust error handling and retry logic
**Key Features**:
- Exception handling patterns
- Retry policies with exponential backoff
- Logging and monitoring
- Circuit breaker pattern

## Common Commands

```bash
# Run sample
npm start

# Run with debugging
npm run debug

# Run tests
npm test

# Lint code
npm run lint

# Clean node_modules
rm -rf node_modules && npm install
```

## Development Tools

### Recommended VS Code Extensions
- JavaScript (ES6) code snippets
- Azure Account
- Azure Tools
- ESLint
- Prettier

### Package Scripts
Each sample includes these npm scripts:
- `npm start` - Run the application
- `npm run debug` - Run with debugging enabled
- `npm test` - Run unit tests
- `npm run lint` - Check code quality
- `npm run format` - Format code with Prettier

## Environment Configuration

### Using .env files
```bash
# .env file example
AZURE_AI_FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
LOG_LEVEL=info
```

### Using environment variables
```bash
# Set environment variables
export AZURE_AI_FOUNDRY_ENDPOINT="your-endpoint"
export AZURE_AI_FOUNDRY_API_KEY="your-api-key"
npm start
```

## Troubleshooting

### Authentication Issues
- Ensure API key is correctly set in environment variables
- Verify Azure CLI login for DefaultAzureCredential
- Check Azure AD permissions and role assignments

### Package Issues
- Clear npm cache: `npm cache clean --force`
- Delete node_modules: `rm -rf node_modules`
- Reinstall packages: `npm install`
- Update packages: `npm update`

### Common Errors
- **Module not found**: Run `npm install` to install dependencies
- **Permission denied**: Check file permissions and authentication
- **Network timeout**: Verify internet connection and proxy settings
- **API quota exceeded**: Check usage limits in Azure portal

## TypeScript Support

All samples include TypeScript support:
- TypeScript definitions included in dependencies
- `tsconfig.json` configuration files
- Type-safe Azure AI SDK usage
- IntelliSense support in VS Code

## Testing

Each sample includes:
- Unit tests with Jest
- Mock implementations for testing
- Integration tests for end-to-end scenarios
- Test coverage reports

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

---

*These JavaScript samples demonstrate modern Node.js patterns and best practices for Azure AI Foundry development.* 