 function EmailManager(command) {
  console.log("EmailManager got:", command);
  
  if (command.includes("send")) {
    return "Email sent successfully.";
  } else if (command.includes("check") || command.includes("inbox")) {
    return "You have 3 new emails: 1 from GitHub, 2 from LinkedIn.";
  } else if (command.includes("delete")) {
    return "Deleted 2 spam emails.";
  } else {
    return "Email command received. Try: 'send email', 'check emails', or 'delete email'";
  }
}

// Simple File Manager
function FileManager(command) {
  console.log("FileManager got:", command);
  
  if (command.includes("list")) {
    return "Files in Documents:\n- report.pdf\n- presentation.pptx\n- photo.jpg\n- notes.txt";
  } else if (command.includes("delete")) {
    return "Which file would you like to delete?";
  } else if (command.includes("search")) {
    return "Searching... Found 5 matching files.";
  } else if (command.includes("create")) {
    return "Created new file.";
  } else {
    return "File command received. Try: 'list files', 'delete file', or 'search files'";
  }
}

// Simple System Status
function SystemStatus() {
  console.log("SystemStatus called");
  
  const status = {
    cpu: "45%",
    memory: "3.2GB/8GB (40%)",
    disk: "128GB free",
    network: "Connected",
    uptime: "5 days, 3 hours"
  };
  
  return `SYSTEM STATUS:
  CPU Usage: ${status.cpu}
  Memory: ${status.memory}
  Disk Space: ${status.disk}
  Network: ${status.network}
  Uptime: ${status.uptime}`;
}

// ========== MAIN TASK ROUTER ==========
export default function TaskRouter(command) {  // REMOVED "async" keyword
  console.log("TaskRouter received command:", command);
  
  // Check if command is valid
  if (!command || typeof command !== "string") {
    return "Please enter a valid command.";
  }
  
  const cleanCommand = command.toLowerCase();
  
  // Simple keyword routing
  if (cleanCommand.includes("email")) {
    return EmailManager(cleanCommand);  // REMOVED "await"
  }
  
  if (cleanCommand.includes("file")) {
    return FileManager(cleanCommand);  // REMOVED "await"
  }
  
  if (cleanCommand.includes("status") || cleanCommand.includes("system")) {
    return SystemStatus();  // REMOVED "await"
  }
  
  if (cleanCommand.includes("help")) {
    return `AVAILABLE COMMANDS:
    
    EMAIL:
    - "check emails" - View your inbox
    - "send email" - Send a new email
    - "delete email" - Delete emails
    
    FILES:
    - "list files" - Show your files
    - "search files" - Find files
    - "create file" - Make a new file
    
    SYSTEM:
    - "system status" - Check computer status
    - "status" - Quick system check
    
    Type any of these commands (with or without / at the start)`;
  }
  
  // Default response for unknown commands
  return `I didn't understand: "${command}"
  
  Try one of these:
  - check emails
  - list files
  - system status
  - help`;
}