from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Header
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets
from typing import Annotated
from service import user as service
from data.user import init_user
from model.user import User, Token

