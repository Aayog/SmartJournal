from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class Emotion(str, Enum):
    JOYFUL = "Joyful"  # 😊
    EXCITED = "Excited"  # 🤩
    CONTENT = "Content"  # ☺️
    GRATEFUL = "Grateful"  # 🙏
    PEACEFUL = "Peaceful"  # 😌
    BORED = "Bored"  # 😐
    CALM = "Calm"  # 😊
    CURIOUS = "Curious"  # 🤔
    CONFUSED = "Confused"  # 😕
    LONELY = "Lonely"  # 😔
    DISAPPOINTED = "Disappointed"  # 😞
    SCARED = "Scared"  # 😨
    FRUSTRATED = "Frustrated"  # 😤
    ANXIOUS = "Anxious"  # 😰
    JEALOUS = "Jealous"  # 😒
    EMBARRASSED = "Embarrassed"  # 😳
    GUILTY = "Guilty"  # 😣

class StoicVirtue(str, Enum):
    WISDOM = "Wisdom"
    COURAGE = "Courage"
    JUSTICE = "Justice"
    TEMPERANCE = "Temperance"

class VirtueAnalysis(BaseModel):
    virtue: StoicVirtue  # The name of the virtue analyzed
    met: bool = Field(default=False, description="Whether the journal entry met the virtue criteria")
    how_met: str = Field(default="", description="Explanation of how the virtue was met, if applicable")
    how_to_improve: str = Field(default="", description="Suggestions for how to better embody the virtue in the future")
    why_not_met: str = Field(default="", description="Reasons why the virtue was not met, if applicable")
    what_to_change: str = Field(default="", description="Suggestions for changes to meet the virtue criteria in the future")
    
    def __repr__(self):
        met_status = "Met" if self.met else "Not Met"
        details = ""
        
        if self.met:
            details = f"How Met: {self.how_met} | How to Improve: {self.how_to_improve}"
        else:
            details = f"Why Not Met: {self.why_not_met} | What to Change: {self.what_to_change}"

        return (f"VirtueAnalysis(Virtue: {self.virtue}, Status: {met_status}, "
                f"Details: {details})")
class JournalEntryAnalysis(BaseModel):
    date: str
    title: str
    emotion: Optional[Emotion] = None
    content: str
    virtues_analysis: List[VirtueAnalysis] = Field(default_factory=list, description="Detailed virtue analyses for the entry")
    summary: Optional[str] = None

    def __repr__(self):
        # Format the primary emotion display
        emotion_display = f"Emotion: {self.emotion.value}" if self.emotion else "Emotion: Not Specified"
        
        # Format the virtues analysis display
        virtues_display = ", ".join([v.virtue for v in self.virtues_analysis]) or "No Virtues Analyzed"
        
        # Prepare a brief version of the content
        content_preview = (self.content[:75] + '...') if len(self.content) > 75 else self.content
        
        # Prepare the summary display
        summary_display = f"Summary: {self.summary}" if self.summary else "Summary: Not Provided"
        
        return (f"JournalEntryAnalysis:\nDate: {self.date}\nTitle: '{self.title}', {emotion_display}\n"
                f"\nContent Preview: '{content_preview}'\nVirtues: {virtues_display}\n{summary_display})")