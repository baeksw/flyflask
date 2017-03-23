# -*- coding:utf-8 -*-
import os
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd

from sqlalchemy import *
from flask import *

from flask_sqlalchemy import SQLAlchemy

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
    
def commit(session):
    try:
        session.commit()
    except Exception as e:
        eprint(e)
        session.rollback()
        session.flush()
