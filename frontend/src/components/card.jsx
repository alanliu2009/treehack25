export function Card({ children, className }) {
    return <div className={`bg-white shadow-md rounded-lg p-4 ${className}`}>{children}</div>;
  }
  
  export function CardHeader({ children, className }) {
    return <div className={`border-b pb-2 mb-2 font-bold text-lg ${className}`}>{children}</div>;
  }
  
  export function CardTitle({ children, className }) {
    return <h2 className={`text-xl font-semibold ${className}`}>{children}</h2>;
  }
  
  export function CardContent({ children, className }) {
    return <div className={`p-2 ${className}`}>{children}</div>;
  }
  