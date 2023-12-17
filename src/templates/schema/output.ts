type Span = {
  text?: string;
  reference?: string; // If the content involves any factual text, a reference must be provided. REMEMBER: Adjacent spans must have distinct references; otherwise, they should be merged into a single span. Each span should have a different reference from each other if any.
};

type Output = {
  content?: Span[];   // what you want to say to the user. 4 - 10 sentences is ok
  actions?: {         // you can use multiple tools at one time
    name: string;
    body?: JSON;      // parameters to call the tool
  }[];
};
