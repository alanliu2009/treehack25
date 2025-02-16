export function Progress({ value, className }) {
  return (
    <div className={`relative w-full bg-gray-300 rounded-lg overflow-hidden ${className}`} style={{ height: "150px"}}>
      <div
        className="h-full transition-all duration-300"
        style={{ width: `${value}%`, backgroundColor: value > 66 ? "green" : value > 33 ? "yellow" : "red" }}
      />
    </div>
  );
}
