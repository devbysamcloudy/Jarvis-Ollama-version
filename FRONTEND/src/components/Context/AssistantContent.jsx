import { createContext, use, useContext, useState } from "react";

const AssistantContext = createContext();

export const AssistantProvider = ({ children }) => {
  const [isAssistantEnabled, setIsAssistantEnabled] = useState(false);
  const [assistantSettings, setAssistantSettings] = useState(true);

  return (
    <AssistantContext.Provider
      value={{
        assistantSettings,
        setAssistantSettings,
        isAssistantEnabled,
        setIsAssistantEnabled,
      }}
    >
      {children}
    </AssistantContext.Provider>
  );
}

export const useAssistantContext = () => useContext(AssistantContext);
export default AssistantContext;