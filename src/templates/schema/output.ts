type Span = {
  text?: string;      // a few words / sentences
  reference?: string; // the url reference related to the text above
};

type Output = {
  content?: Span[];   // what you want to say to the user
  end?: boolean;      // set it to true only when your response can be end with the actions' results directly
  actions?: {         // use one or multiple tools
    name: string;
    body?: JSON;      // parameters to call the tool
  }[];
};
