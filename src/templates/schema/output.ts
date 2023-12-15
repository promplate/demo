type Span = {
  text?: string;
  reference?: string;
};

type Output = {
  content?: Span[]; // what you want to say to the user
  end?: boolean;    // if you want to end your response with the results of the actions, set it to true
  actions?: {       // use the tools
    name: string;
    body?: JSON;    // parameters
  }[];
};
