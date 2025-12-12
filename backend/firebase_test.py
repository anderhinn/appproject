from firebase_api import add_lfg, get_lfg_by_game, send_message, get_messages
from dotenv import load_dotenv
load_dotenv()

def test_lfg():
    print("Testing LFG functions...")
    user_id="mila_test"
    game_id="test_game_123"
    game_name="Test Game"
    note="Looking for group test"

    result=add_lfg(user_id, game_id, game_name, note)
    print("LFG added:", result)

    entries=get_lfg_by_game(game_id)
    print("LFG entries for game:")
    if not entries:
        print("No entries found.")
    else:
        for e in entries:
            print(" - user_id:", e.get("user_id"),
                    " | game_id:", e.get("game_id"),
                    " | note:", e.get("note"),
                    " | id:", e.get("id"))
            
def test_chat():
    print("Testing chat functions...")
    me="mila_test"
    other="other_user"

    chat_id= "_".join(sorted([me, other]))
    print("chat_id:", chat_id)

    send_message(chat_id, me, "Hello from mila_test!")
    send_message(chat_id, other, "Hello from other_user!")

    messages=get_messages(chat_id)
    print("Messages in chat:")
    if not messages:
        print("No messages found.")
    else:
        for m in messages:
            print(f"  [{m.get('timestamp')}] {m.get('sender_id')}: {m.get('text')}")

if __name__ == "__main__":
    test_lfg()
    test_chat()