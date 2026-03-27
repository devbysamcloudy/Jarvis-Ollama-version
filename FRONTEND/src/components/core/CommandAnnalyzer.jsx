
export default function CommandAnalyzer(command) {
  const cleanCommand = command.toLowerCase();
  
  if (cleanCommand.includes("email") || cleanCommand.includes("mail")) {
    return "Email functionality is available. Try: 'check emails' or 'send email'";
  } else if (cleanCommand.includes("file") || cleanCommand.includes("document")) {
    return "File functionality is available. Try: 'list files' or 'organize files'";
  } else if (cleanCommand.includes("system") || cleanCommand.includes("status")) {
    return "System status functionality is available. Try: 'system status'";
  } else if (cleanCommand.includes("help") || cleanCommand.includes("what can you do")) {
    return `Available commands:
    • Email: check emails, send email
    • Files: list files, organize files
    • System: system status
    • Chat: Normal conversation`;
  } else {
    return "I'm not sure how to process that command. Try asking for /help";
  }
}
