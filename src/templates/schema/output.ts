/**
 * This file defines the schema for the output data.
 * It includes the types for spans and the overall output structure.
 */

type Span = {
  text?: string;
  reference?: string; // url related to this span. REMEMBER: Adjacent spans must have distinct references; otherwise, they should be merged into a single span. If the content involves any factual text, a reference must be provided.
};

type Output = {
  content?: Span[];   // what you want to say to the user. 4 - 10 sentences is ok
  end?: boolean;      // set it to true only when your response can be end with the actions' results directly
  actions?: {         // you can use multiple tools at one time
    name: string;
    body?: JSON;      // parameters to call the tool
  }[];
};
