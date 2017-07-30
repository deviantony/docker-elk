import { Request, Response, NextFunction } from 'express';
import validatorMiddleware from './validatorMiddleware';
import { SinonSpy, stub, spy } from 'sinon';
import { expect } from 'chai';

function verifyStoppedTheRequest(nextSpy: SinonSpy): void {
  expect(nextSpy.callCount).to.be.equal(0, 'should not procceed with handling the request');
}

function verifyStatusCode(statusSpy: SinonSpy, expectedCode: number): void {
  expect(statusSpy.callCount).to.be.equal(1, 'should set status code');
  expect(statusSpy.args[0]).to.deep.equal([expectedCode], `status code should be ${expectedCode}`);
}

function verifyRespnse(sendSpy: SinonSpy, expectedResponse: any): void {
  expect(sendSpy.callCount).to.be.equal(1, 'should send response');
  expect(sendSpy.args[0]).to.deep.equal([expectedResponse], 'should send error message');
}

describe('validatorMiddleware', () => {

  let request: Request;
  let statusSpy: SinonSpy;
  let sendSpy: SinonSpy;
  let response: Response;
  let nextSpy: SinonSpy;

  beforeEach(() => {
    request = <any>{
      body: {
        message: 'some message',
        env: 'some env',
        severity: 'some severity',
        timestamp: '2017-07-30T14:24:03',
        version: 'some version'
      }
    };

    statusSpy = spy(() => response);
    sendSpy = spy(() => response);
    response = <any>{
      status: statusSpy,
      send: sendSpy
    };

    nextSpy = spy();
  });

  it('no body should fail', () => {
    request.body = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, 'No log was sent');
  });

  it('no message should fail', () => {
    request.body.message = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'No message was sent. You should use the "message" property to send the message'
      ]
    });
  })

  it('no environment should fail', () => {
    request.body.env = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'No environment was sent. You should use the "env" property to specify the environment'
      ]
    });
  })

  it('no severity should fail', () => {
    request.body.severity = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'No severity was sent. You should use the "severity" property to specify the severity'
      ]
    });
  })

  it('no timestamp should fail', () => {
    request.body.timestamp = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'No timestamp was sent. You should use the "timestamp" property to specify the timestamp'
      ]
    });
  })

  it('invalid timestamp should fail', () => {
    request.body.timestamp = 'invalid';

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'Invalid timestamp was sent'
      ]
    });
  })

  it('no version should fail', () => {
    request.body.version = null;

    validatorMiddleware(request, response, nextSpy);

    verifyStoppedTheRequest(nextSpy);
    verifyStatusCode(statusSpy, 400);
    verifyRespnse(sendSpy, {
      errors: [
        'No version was sent. You should use the "version" property to specify the version'
      ]
    });
  })

  it('all ok should pass the request', () => {
    validatorMiddleware(request, response, nextSpy);

    expect(nextSpy.callCount).to.be.equal(1, 'should pass the request');
    expect(statusSpy.callCount).to.be.equal(0, 'should not set status');
    expect(sendSpy.callCount).to.be.equal(0, 'should not send a response');
  })

});