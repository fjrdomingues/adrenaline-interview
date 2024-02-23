import mermaid from "mermaid"

// One idea to check/evaluate quality is to ask GPT to rate each diagram for the proposed task

const checkMermaidSyntax = async (string) => {
  try {
      await mermaid.parse(string)
      console.log('Syntax is correct.')
  } catch (error) {
      console.error('Syntax error in Mermaid diagram:', error.message)
  }
} 

checkMermaidSyntax(
`
erDiagram
          CUSTOMER }|..|{ DELIVERY-ADDRESS : has
          CUSTOMER ||--o{ ORDER : places
          CUSTOMER ||--o{ INVOICE : "liable for"
          DELIVERY-ADDRESS ||--o{ ORDER : receives
          INVOICE ||--|{ ORDER : covers
          ORDER ||--|{ ORDER-ITEM : includes
          PRODUCT-CATEGORY ||--|{ PRODUCT : contains
          PRODUCT ||--o{ ORDER-ITEM : "ordered in"
`
)