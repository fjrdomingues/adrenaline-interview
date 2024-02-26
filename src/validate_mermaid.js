// import mermaid from "mermaid";
import { run, renderMermaid, parseMMD, cli, error } from "@mermaid-js/mermaid-cli"
import { exec } from 'child_process';

const removeMarkdownWrapper = (string) => {
  // Remove Markdown Mermaid wrapper ```mermaid\n and the closing ```
  return string.replace(/^```mermaid\n?/, '').replace(/\n?```$/, '');
};

const checkMermaidSyntax = async (string) => {
  try {
    // Remove Markdown wrapper if present before parsing
    const mermaidString = removeMarkdownWrapper(string);
    console.log(mermaidString)
    const result = await mermaid.parse(mermaidString);
    console.log(result)
    process.stdout.write('Syntax is correct.\n');
  } catch (error) {
    process.stderr.write(`Syntax error in Mermaid diagram: ${error}\n`);
  }
};

// Read the entire input from stdin
let data = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => {
  data += chunk;
});
process.stdin.on('end', () => {
  // When all data is received, validate the syntax.
  checkMermaidSyntax(data.trim());
});

process.stdin.resume();


const example = 
`\`\`\`mermaid
flowchart TD
  A[Christmas] -->|Get money| B(Go shopping)
  B --> C{Let me think}
  C -->|One| D[Laptop]
  C -->|Two| E[iPhone]
  C -->|Three| F[fa:fa-car Car]
  \`\`\`
`

// try {
//   const result = await mermaid.parse(example);
//   console.log(result)
//   process.stdout.write('Syntax is correct.\n');
// } catch (error) {
//   process.stderr.write(`Syntax error in Mermaid diagram: ${error}\n`);
// }

// const heredocCommand = `cat << EOF | mmdc --input -
// graph TD
//   A[Client] --> B[Load Balancer]
// EOF`;

// exec(heredocCommand, (error, stdout, stderr) => {
//   if (error) {
//     console.error(`exec error: ${error}`);
//     return;
//   }
//   if (stderr) {
//     console.error(`stderr: ${stderr}`);
//     return;
//   }
//   console.log(`stdout: ${stdout}`);
// });

await run(example)

// checkMermaidSyntax(`
// classDiagram
//   class ClientModel {
//       - clientId: String
//       - name: String
//       - email: String
//       - phoneNumber: String
//       - address: String
//       - appointments: List<Appointment>
//       - reviews: List<Review>
//       --
//       + ClientModel(clientId: String, name: String, email: String, phoneNumber: String, address: String)
//       + getClientId(): String
//       + setClientId(clientId: String): void
//       + getName(): String
//       + setName(name: String): void
//       + getEmail(): String
//       + setEmail(email: String): void
//       + getPhoneNumber(): String
//       + setPhoneNumber(phoneNumber: String): void
//       + getAddress(): String
//       + setAddress(address: String): void
//       + getAppointments(): List<Appointment>
//       + setAppointments(appointments: List<Appointment>): void
//       + getReviews(): List<Review>
//       + setReviews(reviews: List<Review>): void
//       + bookAppointment(appointment: Appointment): void
//       + cancelAppointment(appointment: Appointment): void
//       + addReview(review: Review): void
//   }
//   class Appointment {
//       - appointmentId: String
//       - barberId: String
//       - date: Date
//       - time: Time
//       --
//       + Appointment(appointmentId: String, barberId: String, date: Date, time: Time)
//       + getAppointmentId(): String
//       + setAppointmentId(appointmentId: String): void
//       + getBarberId(): String
//       + setBarberId(barberId: String): void
//       + getDate(): Date
//       + setDate(date: Date): void
//       + getTime(): Time
//       + setTime(time: Time): void
//   }
//   class Review {
//       - reviewId: String
//       - barberId: String
//       - rating: int
//       - comment: String
//       --
//       + Review(reviewId: String, barberId: String, rating: int, comment: String)
//       + getReviewId(): String
//       + setReviewId(reviewId: String): void
//       + getBarberId(): String
//       + setBarberId(barberId: String): void
//       + getRating(): int
//       + setRating(rating: int): void
//       + getComment(): String
//       + setComment(comment: String): void
//   }
// `)