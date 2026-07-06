import { Link } from "react-router-dom";

function Breadcrumbs({ items }) {
    return (
        <nav
            className="breadcrumbs"
            aria-label="Breadcrumb"
        >
            {items.map((item, index) => (
                <span key={item.label}>
                    {index > 0 && " / "}

                    {item.to ? (
                        <Link to={item.to}>
                            {item.label}
                        </Link>
                    ) : (
                        item.label
                    )}
                </span>
            ))}
        </nav>
    );
}

export default Breadcrumbs;