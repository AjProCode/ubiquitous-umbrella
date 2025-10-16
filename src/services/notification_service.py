"""Notification service for managing alerts and reminders"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

from ..models.notification import Notification, NotificationType, NotificationPriority
from ..models.product import Product, Medicine


class NotificationService:
    """Service for managing notifications"""
    
    def __init__(self, storage_path: str = "./data"):
        """
        Initialize notification service
        
        Args:
            storage_path: Path to storage directory
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.notifications: List[Notification] = []
        self._load_notifications()
    
    def _load_notifications(self):
        """Load notifications from storage"""
        notifications_file = self.storage_path / "notifications.json"
        if notifications_file.exists():
            try:
                with open(notifications_file, 'r') as f:
                    data = json.load(f)
                    for notif_data in data:
                        notification = self._dict_to_notification(notif_data)
                        if notification:
                            self.notifications.append(notification)
            except Exception as e:
                print(f"Error loading notifications: {e}")
    
    def _save_notifications(self):
        """Save notifications to storage"""
        notifications_file = self.storage_path / "notifications.json"
        try:
            data = [n.to_dict() for n in self.notifications]
            with open(notifications_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving notifications: {e}")
    
    def _dict_to_notification(self, data: Dict[str, Any]) -> Optional[Notification]:
        """Convert dictionary to notification"""
        try:
            return Notification(
                notification_type=NotificationType(data['notification_type']),
                title=data['title'],
                message=data['message'],
                product_barcode=data['product_barcode'],
                priority=NotificationPriority(data['priority']),
                is_read=data.get('is_read', False),
                is_dismissed=data.get('is_dismissed', False),
                created_at=datetime.fromisoformat(data['created_at']),
                scheduled_for=datetime.fromisoformat(data['scheduled_for']) 
                    if data.get('scheduled_for') else None,
                sent_at=datetime.fromisoformat(data['sent_at']) 
                    if data.get('sent_at') else None
            )
        except Exception as e:
            print(f"Error converting dict to notification: {e}")
            return None
    
    def create_expiry_warning(
        self,
        product: Product,
        days_until_expiry: int,
        schedule_days_before: int = 0
    ) -> Notification:
        """
        Create expiry warning notification
        
        Args:
            product: Product about to expire
            days_until_expiry: Days until expiry
            schedule_days_before: Days before to schedule notification
            
        Returns:
            Created notification
        """
        if days_until_expiry <= 0:
            priority = NotificationPriority.CRITICAL
            title = f"⚠️ {product.name} has expired!"
            message = f"{product.name} expired on {product.expiry_date.isoformat()}. Please dispose of it safely."
        elif days_until_expiry == 1:
            priority = NotificationPriority.CRITICAL
            title = f"⚠️ {product.name} expires tomorrow!"
            message = f"{product.name} will expire tomorrow ({product.expiry_date.isoformat()}). Use it immediately."
        elif days_until_expiry <= 3:
            priority = NotificationPriority.HIGH
            title = f"⚠️ {product.name} expires in {days_until_expiry} days"
            message = f"{product.name} will expire on {product.expiry_date.isoformat()}. Prioritize usage."
        else:
            priority = NotificationPriority.MEDIUM
            title = f"📅 {product.name} expires in {days_until_expiry} days"
            message = f"{product.name} will expire on {product.expiry_date.isoformat()}. Plan accordingly."
        
        notification = Notification(
            notification_type=NotificationType.EXPIRY_WARNING,
            title=title,
            message=message,
            product_barcode=product.barcode,
            priority=priority
        )
        
        if schedule_days_before > 0:
            notification.scheduled_for = datetime.now() + timedelta(days=schedule_days_before)
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def create_counterfeit_alert(self, product: Product, details: str = "") -> Notification:
        """
        Create counterfeit alert notification
        
        Args:
            product: Counterfeit product
            details: Additional details
            
        Returns:
            Created notification
        """
        notification = Notification(
            notification_type=NotificationType.COUNTERFEIT_ALERT,
            title=f"🚨 COUNTERFEIT ALERT: {product.name}",
            message=f"The product '{product.name}' (Barcode: {product.barcode}) has been flagged as counterfeit. {details}",
            product_barcode=product.barcode,
            priority=NotificationPriority.CRITICAL
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def create_recall_notification(self, product: Product, recall_reason: str) -> Notification:
        """
        Create recall notification
        
        Args:
            product: Recalled product
            recall_reason: Reason for recall
            
        Returns:
            Created notification
        """
        notification = Notification(
            notification_type=NotificationType.RECALL,
            title=f"🚨 PRODUCT RECALL: {product.name}",
            message=f"{product.name} (Batch: {product.batch_number}) has been recalled. Reason: {recall_reason}",
            product_barcode=product.barcode,
            priority=NotificationPriority.CRITICAL
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def create_medicine_interaction_alert(
        self,
        medicine: Medicine,
        interaction_details: str
    ) -> Notification:
        """
        Create medicine interaction alert
        
        Args:
            medicine: Medicine with interaction
            interaction_details: Interaction details
            
        Returns:
            Created notification
        """
        notification = Notification(
            notification_type=NotificationType.MEDICINE_INTERACTION,
            title=f"⚕️ Drug Interaction Alert: {medicine.name}",
            message=f"Potential drug interaction detected for {medicine.name}: {interaction_details}",
            product_barcode=medicine.barcode,
            priority=NotificationPriority.HIGH
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def create_usage_reminder(
        self,
        product: Product,
        reminder_message: str,
        schedule_for: Optional[datetime] = None
    ) -> Notification:
        """
        Create usage reminder notification
        
        Args:
            product: Product to remind about
            reminder_message: Reminder message
            schedule_for: When to send reminder
            
        Returns:
            Created notification
        """
        notification = Notification(
            notification_type=NotificationType.USAGE_REMINDER,
            title=f"📋 Reminder: {product.name}",
            message=reminder_message,
            product_barcode=product.barcode,
            priority=NotificationPriority.MEDIUM,
            scheduled_for=schedule_for
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def create_recipe_suggestion(
        self,
        products: List[Product],
        recipe_title: str,
        recipe_description: str
    ) -> Notification:
        """
        Create recipe suggestion notification
        
        Args:
            products: Products to use in recipe
            recipe_title: Recipe title
            recipe_description: Recipe description
            
        Returns:
            Created notification
        """
        product_names = ", ".join([p.name for p in products[:3]])
        if len(products) > 3:
            product_names += f" and {len(products) - 3} more"
        
        notification = Notification(
            notification_type=NotificationType.RECIPE_SUGGESTION,
            title=f"👨‍🍳 Recipe Suggestion: {recipe_title}",
            message=f"Try this recipe using {product_names}: {recipe_description}",
            product_barcode=products[0].barcode if products else "",
            priority=NotificationPriority.LOW
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def get_unread_notifications(self) -> List[Notification]:
        """Get unread notifications"""
        return [n for n in self.notifications if not n.is_read and not n.is_dismissed]
    
    def get_pending_notifications(self) -> List[Notification]:
        """Get notifications scheduled to be sent"""
        now = datetime.now()
        return [
            n for n in self.notifications
            if n.scheduled_for and n.scheduled_for <= now and not n.sent_at
        ]
    
    def get_notifications_by_priority(
        self,
        priority: NotificationPriority
    ) -> List[Notification]:
        """Get notifications by priority"""
        return [n for n in self.notifications if n.priority == priority]
    
    def mark_as_read(self, notification: Notification):
        """Mark notification as read"""
        notification.mark_as_read()
        self._save_notifications()
    
    def dismiss(self, notification: Notification):
        """Dismiss notification"""
        notification.dismiss()
        self._save_notifications()
    
    def send_pending_notifications(self) -> List[Notification]:
        """
        Send pending notifications
        
        Returns:
            List of sent notifications
        """
        pending = self.get_pending_notifications()
        sent = []
        
        for notification in pending:
            notification.send()
            sent.append(notification)
            print(f"[{notification.priority.value.upper()}] {notification.title}")
            print(f"  {notification.message}")
            print()
        
        if sent:
            self._save_notifications()
        
        return sent
    
    def clear_old_notifications(self, days: int = 30):
        """
        Clear notifications older than specified days
        
        Args:
            days: Age threshold in days
        """
        cutoff = datetime.now() - timedelta(days=days)
        self.notifications = [
            n for n in self.notifications
            if n.created_at > cutoff or not n.is_dismissed
        ]
        self._save_notifications()
