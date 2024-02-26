"""
Put any code for fine-tuning a model in here. The model can either be an OpenAI model or an open-source
model. Its your job to pick one and justify why it has the best chance at beating GPT-4.
"""

from dotenv import load_dotenv
from openai import OpenAI
import time


# Initialize the OpenAI client
load_dotenv()
client = OpenAI()

def upload_file(file_path):
    """
    Uploads a file to OpenAI and returns the file ID.
    """
    response = client.files.create(
      file=open(file_path, "rb"),  # Specify the correct path to your training dataset
      purpose="fine-tune"
    )
    return response.id


def start_fine_tuning(training_file_id, model="gpt-3.5-turbo"):
    """
    Starts a fine-tuning job using a given training file ID and model.
    """
    job = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=model
    )
    return job


def get_fine_tuning_status(job_id):
    """
    Retrieves the status of a fine-tuning job.
    """
    status = client.fine_tuning.jobs.retrieve(job_id)
    return status


def cancel_fine_tuning(job_id):
    """
    Cancels a fine-tuning job.
    """
    cancel = client.fine_tuning.jobs.cancel(job_id)
    return cancel


def list_fine_tuning_events(job_id, limit=10):
    """
    Lists events for a fine-tuning job.
    """
    events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=limit)
    return events


def delete_fine_tuned_model(model_id):
    """
    Deletes a fine-tuned model.
    """
    delete = client.models.delete(model_id)
    return delete


if __name__ == "__main__":
    job_id = "ftjob-isQ08USSF94GFKlg40CE5zgc"

    if not job_id:
      # Step 1: Upload training and testing datasets
      training_file_id = upload_file('../data/training_dataset.jsonl')
      testing_file_id = upload_file('../data/testing_dataset.jsonl')

      # Step 2: Start fine-tuning the model
      fine_tune_job = start_fine_tuning(training_file_id)

      # Retrieve the job ID and keep track of the status
      job_id = fine_tune_job.id
      print(f"Fine-tuning job {job_id} started!")

    # Step 3: Monitor the fine-tuning job
    while True:
        status_response = get_fine_tuning_status(job_id)

        state = status_response.status
        print(f"Fine-tuning job {job_id} is {state}.")

        info = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id, limit=10)
        print(info)

        if state in ['succeeded', 'failed', 'cancelled']:
            break

        print("Waiting for 30 seconds before the next status check...")
        time.sleep(30)  # Wait for 30 seconds before checking the status again

    # Now the job's final state can be handled
    if status_response.status == 'succeeded':
        print("Fine-tuning job completed successfully.")
    elif status_response.status == 'failed':
        print("Fine-tuning job failed.")


# Model created: ft:gpt-3.5-turbo-0613:rubrick-ai::8wWjQ3wc