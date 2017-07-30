import {
  Request,
  Response,
  NextFunction,
  RequestHandler
} from 'express';
import * as moment from 'moment';

interface ErrorMessages {
  [name: string]: string;
}

const propertyExistanceValidationMessages: ErrorMessages = {
  message: 'No message was sent. You should use the "message" property to send the message',
  env: 'No environment was sent. You should use the "env" property to specify the environment',
  severity: 'No severity was sent. You should use the "severity" property to specify the severity',
  timestamp: 'No timestamp was sent. You should use the "timestamp" property to specify the timestamp',
  version: 'No version was sent. You should use the "version" property to specify the version'
}

export default function validatorMiddleware(req: Request, res: Response, next: NextFunction) {
  if (!req.body) {
    res.status(400).send('No log was sent');
    return;
  }

  const requiredFieldsErrors: string[] = validateRequiredFields(req.body);
  const fieldsFormatErrors: string[] = validateTimestampFormat(req.body);

  const errors: string[] = [];
  errors.push.apply(errors, requiredFieldsErrors);
  errors.push.apply(errors, fieldsFormatErrors);

  if (errors.length > 0) {
    res.status(400).send({ errors: errors });
  } else {
    next();
  }
}

function validateRequiredFields(body: any): string[] {
  const errors: string[] = [];
  for (const name in propertyExistanceValidationMessages) {
    if (!body[name]) {
      const error: string = propertyExistanceValidationMessages[name]
      errors.push(error);
    }
  }

  return errors;
}

function validateTimestampFormat(body: any): string[] {
  if (body.timestamp && !moment(body.timestamp).isValid()){
    return ['Invalid timestamp was sent'];
  }

  return [];
}