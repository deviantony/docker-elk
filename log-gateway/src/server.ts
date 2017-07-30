import { Express, Request, Response } from 'express';
import * as express from 'express';
import * as bodyParser from 'body-parser';
import sendLog from './logstashLogSender';
import validatorMiddleware from './validatorMiddleware';

const server: Express = express();
server.use(bodyParser.json());

server.use('/log', validatorMiddleware);
server.post('/log', (req: Request, res: Response) => {
  const log = req.body;
  console.log('Writing log:', log);

  sendLog(req.body).then(
    () => {
      console.log('Successfully written the log:', log);
      res.status(200).send()
    },
    (error) => {
      console.log('Failed writing log:', log, '\nThe error:', error);
      res.status(500).send(error)
    });
});

const port: number = Number(process.env.LOG_GATEWAY_PORT) || 6000;
server.listen(port, () => console.log('Started listening on port', port));