import time
from openai import OpenAI

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI()

# watch your cost!
# https://openai.com/pricing
# Upload a file with an "assistants" purpose
# file = client.files.create(
#   file=open("webinar.txt", "rb"),
#   purpose='assistants'
# )

# You can also upload new files using curl:
# curl https://api.openai.com/v1/files \
# -H "Authorization: Bearer $OPENAI_API_KEY" \
# -F purpose="assistants" \
# -F file="@/PATH/TO/FILE.txt"

# List all files uploaded to your account
# curl https://api.openai.com/v1/files \    
#  -H "Authorization: Bearer $OPENAI_API_KEY" 


# "file-iDAtEXEDBMlSfuYRgY4F916o"  agentsinproduction.txt
# "file-x5XNjYfQnmJEpSmiJb9tQPPn" webinar.txt
# print(file.id)

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are a teacher assistant chatbot with access to the transcripts of the main teacher webinars. Use your knowledge base to best respond to students' queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=["file-x5XNjYfQnmJEpSmiJb9tQPPn","file-iDAtEXEDBMlSfuYRgY4F916o"]
)
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  # content="What did they say about prompt injection in the webinar?",
  content="What did they say about prompt begging?",
#  file_ids=[file.id]
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Dear Student."
)

# This creates a Run in a queued status. 
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

# periodically retrieve the Run to check on its status to see if it has moved to completed.
while run.status != "completed":
  print(run.status)
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )
  # sleep for 3 seconds
  time.sleep(3)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

# it works, but it's getting empty annotations
# See : https://community.openai.com/t/assistant-citations-annotations-array-is-always-empty/476752
print(messages)