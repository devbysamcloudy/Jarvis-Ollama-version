

const TaskContext = createContext();

export const TaskProvider = ({ children }) => {
  const [isTaskEnabled, setIsTaskEnabled] = useState(false);
  const [taskSettings, setTaskSettings] = useState(true);

  return (
    <TaskContext.Provider
      value={{
        taskSettings,
        setTaskSettings,
        isTaskEnabled,
        setIsTaskEnabled,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
}

export const useTaskContext = () => useContext(TaskContext);