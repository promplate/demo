type Span = {
  text?: string;
  reference?: string;
};

type Output = {
  content: Span[];
  end: boolean;
  action?: {
    name: string;
    body: any;
  }[];
};
