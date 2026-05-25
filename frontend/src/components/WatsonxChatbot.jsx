import { useEffect } from 'react';

const WatsonxChatbot = ({ chatForm = "float" }) => {
  useEffect(() => {
    const LOG = (...args) => console.log("[WatsonxChatbot]", ...args);

    function onChatLoad(instance) {
      LOG("Chat loaded, wiring listeners…");
      instance.on("chat:ready", () => LOG("Chat is ready"));
    }

    // Ensure root container exists OUTSIDE React tree
    let container = document.getElementById("wxochat-root");
    if (!container) {
      container = document.createElement("div");
      container.id = "wxochat-root";
      document.body.appendChild(container); // 👈 append outside React tree
      LOG("Created wxochat-root container outside React");
    }

    // Configure the chatbot
    window.wxOConfiguration = {
      orchestrationID: "7289e58a049a4814bfbcac984cac6840_a90e0f98-20ac-46e4-9230-9c83216f3281",
      hostURL: "https://us-south.watson-orchestrate.cloud.ibm.com",
      rootElementID: "wxochat-root", // 👈 Use the container outside React
      deploymentPlatform: "ibmcloud",
      crn: "crn:v1:bluemix:public:watsonx-orchestrate:us-south:a/7289e58a049a4814bfbcac984cac6840:a90e0f98-20ac-46e4-9230-9c83216f3281::",
      chatOptions: {
        agentId: "5ad2c03a-1caa-4fc6-8f09-b11f364545c5",
      },
      layout: {
        form: chatForm, // 'float' | 'fullscreen-overlay' | 'custom'
        width: "320px",
        height: "530px",
        showOrchestrateHeader: false,
      },
      style: {
        headerColor: "#0f62fe",
        userMessageBackgroundColor: "#e0e0e0",
        primaryColor: "#0f62fe",
      },
    };

    // Load Watsonx script
    const script = document.createElement("script");
    script.src = `${window.wxOConfiguration.hostURL}/wxochat/wxoLoader.js?embed=true`;

    script.addEventListener("load", () => {
      LOG("Loader loaded → init");
      if (window.wxoLoader) {
        window.wxoLoader.init();
      }
    });

    script.addEventListener("error", (e) => {
      console.error("[WatsonxChatbot] loader failed to load", e);
    });

    document.head.appendChild(script);
    LOG("Script added to head");

    // Cleanup function
    return () => {
      LOG("Cleaning up chatbot");
      if (script.parentNode) {
        document.head.removeChild(script);
      }
      if (container && container.parentNode) {
        container.remove(); // clean up container
      }
      delete window.wxOConfiguration;
    };
  }, [chatForm]);

  return null; // This component doesn't render anything visible
};

export default WatsonxChatbot;

// Made with Bob
