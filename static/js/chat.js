const chatApp = Vue.createApp({
    data() {
        return {
            isOpen: false,
            messages: [],
            userInput: '',
            messageId: 0
        }
    },
    methods: {
        toggleChat() {
            this.isOpen = !this.isOpen;
            if (this.isOpen && this.messages.length === 0) {
                this.addMessage("Hello! I'm your AI assistant. How can I help you today?", 'assistant');
            }
        },
        
        addMessage(text, type) {
            this.messages.push({
                id: this.messageId++,
                text: text,
                type: type
            });
            this.$nextTick(() => {
                this.$refs.messageContainer.scrollTop = this.$refs.messageContainer.scrollHeight;
            });
        },
        
        async sendMessage() {
            if (!this.userInput.trim()) return;
            
            const userMessage = this.userInput.trim();
            this.addMessage(userMessage, 'user');
            this.userInput = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage })
                });
                
                const data = await response.json();
                this.addMessage(data.response, 'assistant');
            } catch (error) {
                console.error('Error:', error);
                this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            }
        }
    }
}).mount('#ai-chat');
