import os

from fastapi import FastAPI

from models import TriggerRequest
from models import TriggerResponse


app = FastAPI()


@app.post("/api/v1/trigger",
          status_code=200,
          response_model=TriggerResponse)
async def trigger_spider(payload: TriggerRequest) -> dict:
    async with httpx.AsyncClient() as client:
        if payload.ats_name == 'customrss':
            res = await client.post(
                url=f"{os.getenv('SCRAPY_HOST')}/schedule.json",
                data={
                    'project': os.getenv('SCRAPY_PROJECT'),
                    'spider': CUSTOM_RSS.get(
                        f'{payload.company_id}-{payload.scrape_id}'
                    ),
                    'company_id': payload.company_id,
                    'scrape_id': payload.scrape_id,
                    'start_url': payload.start_url,
                    'ats_name': payload.ats_name,
                    **payload.params,
                }
            )
        else:
            res = await client.post(
                url=f"{os.getenv('SCRAPY_HOST')}/schedule.json",
                data={
                    'project': os.getenv('SCRAPY_PROJECT'),
                    'spider': payload.ats_name,
                    'company_id': payload.company_id,
                    'scrape_id': payload.scrape_id,
                    'start_url': payload.start_url,
                    'ats_name': payload.ats_name,
                    **payload.params,
                }
            )
    return {
        'task_id': res.json().get('jobid'),
        'message': 'success'
    }