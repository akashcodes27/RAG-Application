css = """
<style>
/* ── Page & font ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Chat messages ───────────────────────────────── */
.chat-message {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
    background: #1e2a3a;
    flex-direction: row-reverse;
}

.chat-message.bot {
    background: #12202f;
}

/* ── Avatar ──────────────────────────────────────── */
.chat-message .avatar {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
}

.chat-message .avatar img {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #2e4060;
}

/* ── Message bubble ──────────────────────────────── */
.chat-message .message {
    flex: 1;
    padding: 10px 14px;
    border-radius: 8px;
    color: #e8edf2;
    font-size: 0.95rem;
    line-height: 1.6;
    background: #1a2d42;
}

.chat-message.user .message {
    background: #1f4068;
    text-align: right;
}

/* ── Badge for agent type ────────────────────────── */
.agent-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 4px;
    letter-spacing: 0.04em;
}

.agent-badge.pdf  { background: #1a4a3a; color: #4ecca3; }
.agent-badge.sql  { background: #1a2a4a; color: #4eb8cc; }
</style>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png"
             alt="AI" />
    </div>
    <div class="message">
        <span class="agent-badge {{BADGE_CLASS}}">{{BADGE_LABEL}}</span><br>
        {{MSG}}
    </div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png"
             alt="User" />
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""
