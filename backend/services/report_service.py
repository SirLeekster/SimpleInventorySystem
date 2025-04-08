from backend.database import db
from backend.models.inventory_item import Inventory_Item
from backend.models.Sale import Sale
from sqlalchemy import func
from datetime import datetime, timedelta
from collections import defaultdict


def get_sales_report_for_org(organization_id, range_code="7d"):
    now = datetime.utcnow()

    # Convert range code into timedelta
    ranges = {
        "1d": now - timedelta(days=1),
        "7d": now - timedelta(days=7),
        "30d": now - timedelta(days=30),
        "1y": now - timedelta(days=365)
    }

    start_date = ranges.get(range_code, now - timedelta(days=7))  # fallback = 7d

    # Total sales amount for this range
    total_sales = db.session.query(func.coalesce(func.sum(Sale.price), 0)).filter(
        Sale.organization_id == organization_id,
        Sale.sold_at >= start_date
    ).scalar()

    # Most sold item in this range
    top_item_row = db.session.query(
        Inventory_Item.product_name,
        func.count(Sale.id).label("count")
    ).join(Sale, Sale.inventory_id == Inventory_Item.id).filter(
        Inventory_Item.organization_id == organization_id,
        Sale.sold_at >= start_date
    ).group_by(Inventory_Item.product_name).order_by(func.count(Sale.id).desc()).first()

    top_item = top_item_row[0] if top_item_row else "N/A"

    # Sales this week (fixed to 7 days from now regardless of filter)
    week_sales = db.session.query(func.count()).filter(
        Sale.organization_id == organization_id,
        Sale.sold_at >= now - timedelta(days=7)
    ).scalar()

    # Daily trend query (only returns days with sales)
    trend_rows = db.session.query(
        func.date(Sale.sold_at).label("date"),
        func.sum(Sale.price).label("sales")
    ).filter(
        Sale.organization_id == organization_id,
        Sale.sold_at >= start_date
    ).group_by(func.date(Sale.sold_at)).order_by(func.date(Sale.sold_at)).all()

    # Build full trend data with 0 fill for days with no sales
    sales_map = defaultdict(float)
    for row in trend_rows:
        sales_map[row.date] = float(row.sales)

    trend = []
    date_cursor = start_date.date()
    today = now.date()
    while date_cursor <= today:
        trend.append({
            "date": str(date_cursor),
            "sales": round(sales_map[date_cursor], 2) if date_cursor in sales_map else 0.0
        })
        date_cursor += timedelta(days=1)

    return {
        "summary": {
            "total_sales": round(total_sales, 2),
            "top_item": top_item,
            "week_sales": week_sales
        },
        "trend": trend
    }
