import argparse
from openai import OpenAI

APIKEY = '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'
chat_history = []  # This is managed by your application, outside of the LLM

def generate_response(model, system_prompt, user_message, chat_history):
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    for entry in chat_history:
        messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": user_message})

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=APIKEY)

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "agentwriter.xyz", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "agentwriter", # Optional. Site title for rankings on openrouter.ai.
        },
        model=model,
        messages=messages
    )

    response_content = completion.choices[0].message.content

    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role":"assistant", "content": response_content})
    return response_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", help="chapter")
    parser.add_argument("--scene", help="scene")

    args = parser.parse_args()
    if not args.chapter or not args.scene:
        print("you must provide chapter and scene number")
        exit()

    codex = ""
    with open('codex.txt', 'r') as fp:
        codex = fp.read()

    model= "openai/gpt-4o-mini"
    system_prompt = ""
    with open('system_prompts/generate_scene_brief.txt', 'r') as fp:
        system_prompt = fp.read()
        system_prompt += f'\n[CODEX]\n{codex}\n[/CODEX]'

    with open('user_prompts/generate scene brief.txt', 'r') as fp:
        user_message = fp.read()
        user_message = user_message.replace('%%CHAPTER%%', args.chapter)
        user_message = user_message.replace('%%SCENE%%', args.scene)

    with open('scene_briefs.md', 'a') as fp:
        res = generate_response(model, system_prompt, user_message, chat_history)
        print(res)
        print('\n---')
        fp.write(res)
        fp.write('\n---')

    model= "anthropic/claude-3.7-sonnet:beta"
    system_prompt = ""
    with open('system_prompts/dev_editor.txt', 'r') as fp:
        system_prompt = fp.read()
        system_prompt.replace('%%CODEX', codex)
    system_prompt += f'\n[CODEX]\n{codex}\n[/CODEX]'

    with open('user_prompts/eval scene brief.txt', 'r') as fp:
        user_message = fp.read()

    with open('scene_briefs.md', 'a') as fp:
        res = generate_response(model, system_prompt, user_message, chat_history)
        print(res)
        print('\n---')
        fp.write(res)
        fp.write('\n---')
    

    with open('user_prompts/rewrite scene brief.txt', 'r') as fp:
        user_message = fp.read()

    with open('scene_briefs.md', 'a') as fp:
        res = generate_response(model, system_prompt, user_message, chat_history)
        print(res)
        print('\n---')
        fp.write(res)
        fp.write('\n---')
    

    system_prompt = ""
    with open('system_prompts/active_scene_beats.txt', 'r') as fp:
        system_prompt = fp.read()
        system_prompt.replace('%%CODEX', codex)
    system_prompt += f'\n[CODEX]\n{codex}\n[/CODEX]'

    with open('user_prompts/rewrite beats.txt', 'r') as fp:
        user_message = fp.read()

    with open('scene_briefs.md', 'a') as fp:
        res = generate_response(model, system_prompt, user_message, chat_history)
        print(res)
        print('\n---')
        fp.write(res)
        fp.write('\n---')
    
