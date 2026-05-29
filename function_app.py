import azure.functions as func
import json
import os
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="recommendations/{user_id}")
def recommendations(req: func.HttpRequest) -> func.HttpResponse:

    user_id = req.route_params.get("user_id")

    try:
        # Connection Azure Blob
        connection_string = os.environ["AzureWebJobsStorage"]

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        blob_client = blob_service_client.get_blob_client(
            container="recommendations",
            blob="recommendations.json"
        )

        # Télécharger JSON
        blob_data = blob_client.download_blob().readall()

        recommendations_dict = json.loads(blob_data)

        # Fallback user inconnu
        if user_id not in recommendations_dict:
            user_id = "-1"

        result = {
            "user_id": user_id,
            "recommendations": recommendations_dict[user_id]
        }

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500
        )
#push
