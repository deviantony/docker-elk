import * as request from 'request';

const logstashUrl: string = process.env.LOGSTASH_URL || 'http://localhost:9191/mw';
console.log('Will write logstash logs to', logstashUrl);

export default async function sendLog(log: any): Promise<void> {
  return new Promise<void>((resolve, reject) => {
    const options: request.UrlOptions & request.CoreOptions = {
      url: logstashUrl,
      json: log
    }

    request.put(options, (error: any, response: request.RequestResponse) => {
      if (!error) {
        resolve();
      } else {
        reject(error);
      }
    })
  });
}