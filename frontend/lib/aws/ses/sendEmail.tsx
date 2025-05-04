"use server"
import type { SendEmailCommandInput } from "@aws-sdk/client-ses";
import { SES } from "@aws-sdk/client-ses";

const ses = new SES({ region: process.env.AWS_SES_REGION });

const logoLink = "https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0588111d-fd5e-4f52-b979-a05fdbaf8ee5_3496x2784.png"

export async function sendAWSEmail(toEmail: string, subject: string) {
    const emailHtml = `    <div style="background-color: #9bb4dd; padding: 20px; font-family: Arial, sans-serif; color: #333;">
        <div
            style="max-width: 600px; margin: 0 auto; border-radius: 8px; background-color: #ffffff; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <img src="${logoLink}" alt="Quantoflow Logo"
                style="width: 150px; margin-bottom: 20px;" />
            <h2 style="color: #333; font-size: 24px; font-weight: bold;">Welcome to Know Your Founder</h2>
            <p style="font-size: 16px; line-height: 1.6; color: #666;">Hello,</p>
            <p style="font-size: 16px; line-height: 1.6; color: #666;">Your administrator has created an account for
                you.
            </p>
            <p style="font-size: 16px; line-height: 1.6; color: #666;">You can now log in by clicking the link below:
            </p>
            <a href="https://app.quantoflow.com/" target="_blank"
                style="display: inline-block; margin-top: 15px; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #9bb4dd; border-radius: 5px; text-decoration: none;">Login
                Here</a>
            <p style="font-size: 12px; line-height: 1.4; color: #999; margin-top: 20px;">If you have any questions, feel
                free to contact support.</p>
        </div>
    </div>`
    const params: SendEmailCommandInput = {
        Source: "michael@quantoflow.com",
        Destination: {
            ToAddresses: [toEmail],
        },
        Message: {
            Body: {
                Html: {
                    Charset: "UTF-8",
                    Data: emailHtml,
                },
            },
            Subject: {
                Charset: "UTF-8",
                Data: subject,
            },
        },
    };

    await ses.sendEmail(params);
    console.log(`successfully sent email to: ${toEmail}`)
}


export async function sendClientPortalEmail(toEmail: string, subject: string, name: string, formLink: string) {

    const emailHtml = ` <div style="background-color: #9bb4dd; padding: 20px; font-family: Arial, sans-serif; color: #333;">
  <div
      style="max-width: 600px; margin: 0 auto; border-radius: 8px; background-color: #ffffff; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
      <img src="${logoLink}" alt="Quantoflow Logo"
          style="width: 150px; margin-bottom: 20px;" />
      <h2 style="color: #333; font-size: 24px; font-weight: bold;">Welcome to Know Your Founder</h2>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">Hello ${name},</p>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">
      We have created a client portal to collect information about your business to fulfill new regulatory requirements
      </p>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">You can now log in and submit documents by clicking the link below:
      </p>
      <a href="${formLink}" target="_blank"
          style="display: inline-block; margin-top: 15px; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #9bb4dd; border-radius: 5px; text-decoration: none;">Login
          Here</a>
      <p style="font-size: 12px; line-height: 1.4; color: #999; margin-top: 20px;">If you have any questions, feel
          free to contact support.</p>
  </div>
</div>`
    const params: SendEmailCommandInput = {
        Source: "michael@quantoflow.com",
        Destination: {
            ToAddresses: [toEmail],
        },
        Message: {
            Body: {
                Html: {
                    Charset: "UTF-8",
                    Data: emailHtml,
                },
            },
            Subject: {
                Charset: "UTF-8",
                Data: subject,
            },
        },
    };

    await ses.sendEmail(params);
    console.log(`successfully sent email to: ${toEmail}`)
}

export async function sendReviewEmail(toEmail: string, subject: string, reviewLink: string) {

    const emailHtml = ` <div style="background-color: #9bb4dd; padding: 20px; font-family: Arial, sans-serif; color: #333;">
  <div
      style="max-width: 600px; margin: 0 auto; border-radius: 8px; background-color: #ffffff; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
      <img src="${logoLink}" alt="Quantoflow Logo"
          style="width: 150px; margin-bottom: 20px;" />
      <h2 style="color: #333; font-size: 24px; font-weight: bold;"></h2>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">Hello,</p>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">
     A new CDD case awaits approval
      </p>
      <p style="font-size: 16px; line-height: 1.6; color: #666;">You can now log in and submit documents by clicking the link below:
      </p>
      <a href="${reviewLink}" target="_blank"
          style="display: inline-block; margin-top: 15px; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #9bb4dd; border-radius: 5px; text-decoration: none;">Go to case</a>

  </div>
</div>`
    const params: SendEmailCommandInput = {
        Source: "michael@quantoflow.com",
        Destination: {
            ToAddresses: [toEmail],
        },
        Message: {
            Body: {
                Html: {
                    Charset: "UTF-8",
                    Data: emailHtml,
                },
            },
            Subject: {
                Charset: "UTF-8",
                Data: subject,
            },
        },
    };

    await ses.sendEmail(params);
    console.log(`successfully sent email to: ${toEmail}`)
}