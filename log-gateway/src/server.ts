import { Express, Request, Response } from 'express';
import * as express from 'express';
import * as bodyParser from 'body-parser';
import sendLog from './logstashLogSender';

const server: Express = express();
server.use(bodyParser.json());

server.post('/log', (req: Request, res: Response) => {
  const log = req.body;
  console.log('Writing log:', log);

  sendLog(req.body).then(
    () => {
      console.log('Successfully written the log:', log);
      res.status(200).send()
    },
    (error) => {
      console.log('Failed writing log:', log);
      res.status(500).send()
    });
});

const port: number = Number(process.env.LOG_GATEWAY_PORT) || 9595;
server.listen(port, () => console.log('Started listening on port', port));