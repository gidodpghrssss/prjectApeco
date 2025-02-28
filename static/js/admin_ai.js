class AdminAIAgent {
    constructor() {
        this.currentTool = null;
        this.chatMessages = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Tool selection
        document.querySelectorAll('.list-group-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.selectTool(e.target.dataset.tool);
            });
        });

        // Send message
        document.getElementById('send-button').addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key support
        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    selectTool(tool) {
        this.currentTool = tool;
        this.updateToolWorkspace();
    }

    async sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessageToChat('user', message);
        input.value = '';

        try {
            const response = await fetch('/api/admin/ai/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tool: this.currentTool,
                    query: message
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.addMessageToChat('agent', data.response);
                if (data.visualization) {
                    this.displayVisualization(data.visualization);
                }
            } else {
                this.addMessageToChat('error', data.error || 'An error occurred');
            }
        } catch (error) {
            this.addMessageToChat('error', 'Failed to communicate with the AI agent');
        }
    }

    addMessageToChat(type, content) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    updateToolWorkspace() {
        const workspace = document.getElementById('tool-workspace');
        workspace.innerHTML = ''; // Clear current workspace
        
        switch(this.currentTool) {
            case 'database':
                this.setupDatabaseWorkspace(workspace);
                break;
            case 'files':
                this.setupFileWorkspace(workspace);
                break;
            case 'calculator':
                this.setupCalculatorWorkspace(workspace);
                break;
            case 'visualization':
                this.setupVisualizationWorkspace(workspace);
                break;
            case 'valuation':
                this.setupValuationWorkspace(workspace);
                break;
            case 'market':
                this.setupMarketWorkspace(workspace);
                break;
            case 'documents':
                this.setupDocumentWorkspace(workspace);
                break;
        }
    }

    setupDatabaseWorkspace(workspace) {
        // Implement database management interface
    }

    setupFileWorkspace(workspace) {
        // Implement file management interface
    }

    setupCalculatorWorkspace(workspace) {
        // Implement calculator interface
    }

    setupVisualizationWorkspace(workspace) {
        // Implement visualization interface
    }

    setupValuationWorkspace(workspace) {
        // Implement valuation interface
    }

    setupMarketWorkspace(workspace) {
        // Implement market analysis interface
    }

    setupDocumentWorkspace(workspace) {
        // Implement document processing interface
    }

    displayVisualization(data) {
        const workspace = document.getElementById('tool-workspace');
        // Handle different types of visualizations (charts, graphs, etc.)
    }
}

// Initialize the AI agent when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.adminAI = new AdminAIAgent();
});
