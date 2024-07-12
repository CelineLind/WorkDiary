import gradio as gr

def submit(input_text):
    return input_text

# Layout
with gr.Blocks() as home:
    # Yesterday tab layout
    with gr.Tab("Yesterday"):
        gr.Markdown("Yesterday")

    # Today tab layout
    with gr.Tab("Today"):
        gr.Markdown("What did you do today?")
        input_text = gr.Textbox(label="Today I...")
        updatebtn = gr.Button("Save")
        display_output = gr.Textbox(label="You submitted...")
        # Submit/Update entry
        updatebtn.click(submit, inputs=input_text, outputs=display_output)

    # Select date tab layout
    with gr.Tab("Select Date"):
        gr.Markdown("Select Date")

    with gr.Row(equal_height=True):
        exportbtn = gr.Button("Export current entry")
        multiplebtn = gr.Button("Export multiple dates")
        searchbtn = gr.Button("AI search")

# Launch app
home.launch()