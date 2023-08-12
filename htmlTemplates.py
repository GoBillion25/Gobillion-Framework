bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://gobillion-images-production.s3.ap-south-1.amazonaws.com/icons/customerSupport.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://gobillion-images-production.s3.ap-south-1.amazonaws.com/question.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}
.stApp > div[data-testid="stBlock"] {
            flex: 1;
        }
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.user-input-container {
    padding: 1rem;
    background-color: #fff;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 80%;
}

.chat-message.user {
    background-color: #f0f0f0;
    color: #000;
    justify-content: flex-end;
    align-self: flex-end;
    margin-left: auto;
}

.chat-message.bot {
    background-color: #e0e0e0;
    color: #000;
    justify-content: flex-start;
    align-self: flex-start;
    margin-right: auto;
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 0 1rem;
    border-radius: 0.5rem;
}

.user-input-container .avatar {
    width: 20%;
}

.user-input-container .avatar img {
    max-width: 40px;
    max-height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.user-input-container input[type="text"] {
    flex: 1;
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: 1px solid #ccc;
    margin-left: 1rem;
}
.footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 10px;
            background-color: #f0f0f0;
            text-align: center;
        }

.user-input-container button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.5rem;
    background-color: #007bff;
    color: #fff;
    cursor: pointer;
}
</style>
'''
