from enum import Enum


class MESSAGES(str, Enum):
    DEFAULT = lambda msg="": f"{msg if msg else ''}"
    MODEL_ADDED = lambda model="": f"The model '{model}' has been added successfully."
    MODEL_DELETED = (
        lambda model="": f"The model '{model}' has been deleted successfully."
    )


class WEBHOOK_MESSAGES(str, Enum):
    DEFAULT = lambda msg="": f"{msg if msg else ''}"
    USER_SIGNUP = lambda username="": (
        f"New user signed up: {username}" if username else "New user signed up"
    )


class ERROR_MESSAGES(str, Enum):
    def __str__(self) -> str:
        return super().__str__()

    DEFAULT = lambda err="": f"Something went wrong :/\n{err if err else ''}"
    ENV_VAR_NOT_FOUND = "Required environment variable not found. Terminating now."
    CREATE_USER_ERROR = "Oops! Something went wrong while creating your account. Please try again later. If the issue persists, contact support for assistance."
    DELETE_USER_ERROR = "Oops! Something went wrong. We encountered an issue while trying to delete the user. Please give it another shot."
    EMAIL_MISMATCH = "Uh-oh! This email does not match the email your provider is registered with. Please check your email and try again."
    EMAIL_TAKEN = "Uh-oh! This email is already registered. Sign in with your existing account or choose another email to start anew."
    USERNAME_TAKEN = (
        "Uh-oh! This username is already registered. Please choose another username."
    )
    COMMAND_TAKEN = "Uh-oh! This command is already registered. Please choose another command string."
    FILE_EXISTS = "Uh-oh! This file is already registered. Please choose another file."

    NAME_TAG_TAKEN = "Uh-oh! This name tag is already registered. Please choose another name tag string."
    INVALID_TOKEN = (
        "Your session has expired or the token is invalid. Please sign in again."
    )
    INVALID_CRED = "The email or password provided is incorrect. Please check for typos and try logging in again."
    INVALID_EMAIL_FORMAT = "The email format you entered is invalid. Please double-check and make sure you're using a valid email address (e.g., yourname@example.com)."
    INVALID_PASSWORD = (
        "The password provided is incorrect. Please check for typos and try again."
    )
    INVALID_TRUSTED_HEADER = "Your provider has not provided a trusted header. Please contact your administrator for assistance."

    EXISTING_USERS = "You can't turn off authentication because there are existing users. If you want to disable WEBUI_AUTH, make sure your web interface doesn't have any existing users and is a fresh installation."

    UNAUTHORIZED = "401 Unauthorized"
    ACCESS_PROHIBITED = "You do not have permission to access this resource. Please contact your administrator for assistance."
    ACTION_PROHIBITED = (
        "The requested action has been restricted as a security measure."
    )

    FILE_NOT_SENT = "FILE_NOT_SENT"
    FILE_NOT_SUPPORTED = "Oops! It seems like the file format you're trying to upload is not supported. Please upload a file with a supported format (e.g., JPG, PNG, PDF, TXT) and try again."

    NOT_FOUND = "We could not find what you're looking for :/"
    USER_NOT_FOUND = "We could not find what you're looking for :/"
    API_KEY_NOT_FOUND = "Oops! It looks like there's a hiccup. The API key is missing. Please make sure to provide a valid API key to access this feature."

    MALICIOUS = "Unusual activities detected, please try again in a few minutes."

    PANDOC_NOT_INSTALLED = "Pandoc is not installed on the server. Please contact your administrator for assistance."
    INCORRECT_FORMAT = (
        lambda err="": f"Invalid format. Please use the correct format{err}"
    )
    RATE_LIMIT_EXCEEDED = "API rate limit exceeded"

    MODEL_NOT_FOUND = lambda name="": f"Model '{name}' was not found"
    OPENAI_NOT_FOUND = lambda name="": "OpenAI API was not found"
    OLLAMA_NOT_FOUND = "WebUI could not connect to Ollama"
    CREATE_API_KEY_ERROR = "Oops! Something went wrong while creating your API key. Please try again later. If the issue persists, contact support for assistance."

    EMPTY_CONTENT = "The content provided is empty. Please ensure that there is text or data present before proceeding."

    DB_NOT_SQLITE = "This feature is only available when running with SQLite databases."

    INVALID_URL = (
        "Oops! The URL you provided is invalid. Please double-check and try again."
    )




class USER_CONSTANTS(str, Enum):
    AVATOR_IMAGE = (
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/wAARCABkAGQDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAABwAFBggJBAMC/8QAORAAAgEDAwIFAgQFAwMFAAAAAQIDBAURBhIhAAcIEyIxQRRRFTJhgRYjQnGRJFKxFzNyGEPBwtP/xAAdAQABBQEBAQEAAAAAAAAAAAAEAwUGBwgCAQAJ/8QANxEAAQIFAgQEAwcDBQAAAAAAAQIRAAMEBSESMQZBUWETInGBMlKxFEKRocHR8AcVYhYjJDPx/9oADAMBAAIRAxEAPwCrfZTwHa17qWS3X25XaezwXJg6CGhWqaGDgtI6GVGOAykrGHI3AHB4EU0/YtDeHXuZXWXv/wBp07hUTUINHS0t9qLZHuZhibeiiQ42uuxgpzz9s377Fd3tJ6Q0Na7XrWjGm9SxUM2+rqph59KZF3D6YSq8SEqzCTABJCghscADul2kl8R+obZf9M30jSNpkqVa4SwKZp98iApCsSKrEBGwAAoAHtkZY6e9yyELmTAUl36DD4I7hubxZ114IlrpVpo5agtOjSXLrBLEkEsNweTbERVnvDqPtvrfVKXLtH2mm0Pavp1ja1i7zXPdIM5kEkqhxnI4yRx8dcunuxHeTVVHFctOdqNU3SlnXfHNSWuaVHX7hlUgjrQ3t74b9Cdr4BX2wi3z0pXz6+tkVJMFTuUyOAEDA4JxjgHHz1P9J2Cw11cNX9rLxpe6UdEf9XbqPyZlnc4JV3jI2kcgEqcn5x0grjmySZxlTZjBJYqIwOWemf8AyAJPAkiUlKKurAmKGAA+eWSRv6N7RnnYfBf4hrrSQ1n/AE0ajNQ5jjguVypqKoLc8eTNIsnwT+XnHVn9T37xuap7GnsvVdpe10enamgitYq6KG3CYpGFIKAVBgRyFHqSIFSdybGCkHC4y/x1UU0tq0WsNpULRPTW6oHnoxk2tPIzMDtDBwNhLcEk9F/tp2e0JV6nkqbrBUTXKWghrKWmnqpHh+nYsgmWBiVSTgqxAzgj2LMDJJd1oKmoVIpleIUuCxGCGcGCazgq126n8asmTCobgBLj69ucZHTeDTxAqrH+CaUjPv8Ai9H/APr01XPwj9/rZQTXGXQbzxwjLJSVtPUSn/xjjdnb9getua7tHTXK7Y/h6ltlnopXaV22PPW7QpTYFyEjJLZLHd6cbQDuAQuPbyyVdRadRrtnobuJ56aNJD5QDsfLyvsT5XBBBAYHHOD0tXXCnoadU+YDgPgj9o7t3DPD1zSRLmzAoDqkhyCWwGdkks/bfbHy7dmu61mo5rjde3moaSmp1LSyy26VUQfckrgdQ+tpWimIFLNAvGElOWHH3wP+Otf9V2PQfb8x1Nwt+l9M/US+TFcqs09G0rH8zKOHcgE5IwDgjPUI1X2w0Br6lajv+l49WCqRB+OUxpw0ZAONro3m4AOQD6RxnPTXZOIKC+HRLVpVyfIPvCNZwNTeCtdFVBS07pLbeoOPQiMz7xoHUVgp6Wpu1EsKVqCSJRKjMVKhgSoJIG0g89ckFollhJihZzj2UZPVte5HhKn0xablJoySW9JUNGKOkrWK1FKAWL7CpCyHaqr7ZPOB0f8Awu+GN6OzLbEo6a235aQrd66WBJZ0lb1CFN4bZsBALRlSQwzg9T1PDqpi9ZOiWzknLZbkA5O+ORDxSVZflUCjSqT4k/UUhIGl8O+SWA2c7naM5dZ6dt6VVDc7Dap6SiutK9VHSnc5gAqJoQpJLHOIg3JP5s8AgBdbFXLwy6Zt0kMFXqDE5hVpXlqjGZHOdzhS3AJzgDge3S6OmWK2VCvFFSQ/IS8e3mhrk3m9U6BKNKktzM1z2c6MsMPz3ivmt9Uw+I68aetuk+3tHFbaOrSmvNVLCE/DZYSDIWjRh6nXcuCcHkA8A9Tm1aDuFmt38N6SuddaIrfE70lJTPGtI3pyZFQgspDZ/MxPPzz1x+Ertsl3oKi46YdErtTot6qUrqnfLh1DeWCvLKMuQxGfVg5PTvq68S6fsGoL7ebRUUFfbrfPEYHDgrwTlMgZDYBDfIHxyOsbXOuutGt7diSklKcFyvUHV0GklhyYO2Y2FbRKnSVrnsZhQDp+VJGB1LgOXJ6coqD3V7h6v789zrD2Z/FJ6ijW4RWupkiYL9VcGOJpmA4YR+pVX2wp+/Vqu/nb7tx4Kbj2k1X2toBbHq7i1p1FM1Q4W6UexN7zKSRlSxcYAxjHWYNm1PXab1dbtUxTSNU2+tiqwQ5DMysGPq9+eef16O/il8V1w8RmoLTR0tPU01js0G2ngkfJkncDzJMfH+0foOtAy7JRKtEy3zwFBYIW4+Iq+JR7kuX6tFBV1dUTa1M1OANuzbD0ZgBGrU8ts05p03a2UayUilJ0WkgABR3B37R8ANuJ+wJ6c6r6HW1/otT6a1+lrvlppZYqT6cpImHMZCVEfu6Eq+VJBGRjBBzE6yi1zctC6YptBVUMNXOtFHVGUgbKVo8SMuRy44I6eY+2VRZNPWiSS2x014gamNTJRyCEysCFl3OBlwAWbB9yP16zVwPxZL4Vt6pxUZhMzzAO6AzAqPwnV0cc3izZU+XP/wC46V7A4LhQOoEHkGz1eOrWHd7uncLSdHz9vmtM9fPNR1l+p61JaWCkV2V54hxIHZBlAwGCefbqIVGpW17caa52iga36OtdQGjmPDVRjTAWBR+WEFAN39XOOOevW5NqTVMo0RVfXWqVqeeomrFjVoZfLkCKq5+HZt+DyVXB/Men27WxbFoiS3RpNO1JbnpUlRQGz5JTeVGAB8nHtz9upLxn/UhE6mFLRKBKxuMMCGcHZ+XZtng9MmmtEkeCkCZ5tiSMjfJOcAActwMxXDwraI7b+Mu+9z+4Hdy3NqCOkrI7ZYIZp5ES3UDCTyyiBhhyEUknPOc9V27S3tvDj321P2rvV1aSzwXkW9I9+9IWeQiOTPtnaVB+5PQ28LvivvHhqv8AdnajqrjZrxT7KmjhmEZEy/8AbkGRjI5B/QnoT6r15dNe65vOrpyaaa81clY8cTEKhJyv+OOfv1oCVRUtPRIppAACQAB0Yb+r59Yqa13Oqo7kag5BB576gze37RqbqGG2yzSzU708qR/96RZdzq2SAu33xk+/t9unLthqu+0Fpq30faLVR3KGaWjklq/MleKMhWDKqZUtuBByQCQvP2bNOVVrOiLTqGqhzNVW2lYGGIF5DtUKpzy3v1CL/oWpqq2OK30N/s11uoaRyS9NNJs27WDq23n15+4x1YvDk1VfQCVO5gb9t39oifGlOmmqE3GV91we+rvyy2YIF2sWma+7Vlx7houqLtVSCQ1dfmNoo9igRIinCxghmAHtvPuckrqomvl1/Q6lqaa3atuEsCM6K01SXJCyMgII+CFDfpuI6XUnNKmV5NK8dMD2zFcpvUyaNaTKAPUl/fyxZbsV3dsXbz6i4vTzwX0WmAUNpoKcxDLecDH5RHpjUrjaR6cDgsFHTvrGu1v3EuNZDrHTMVNUXGjdHlHnL5YO5o43EmQ2MuMqTtyBgAg9AvtTDbUstNsusNwrKClW3Lcrf5jI5yDmNnVS21lHqK4BDfr0NdR+Lnux2Z1xeNJ0sKXi0NWGsjhvMszMqSxo3kq8Ui+iN9ygAkZGDnrEJtlfcKhdsoVadA1DUMEvv25d85cYO3LvXoscuTc/CczEpSSDsNOAOzPAis3ZK83DUtbb6ukKG2PJT1AwcLKjYxhgDgjkH7dSbsZ2Y/H+/FLQVkohs1iqEuNyqSuVjjjYEJ7EFmYBQp98nHPVhKnuZoXUtbaNTd2ezuo7NW3S3CQVVqq5D9SrYZX2RtTMygHgNI+M/Pv1K+3/AHP7F6UlekgvFssqxzfVCjrbBXLOy8r5ksqtMJZfgSO5AHx89TS8328i0GQmhWmpUCCzFILZIKXf/FwM+kQ1dFaq+mR9kIDKcqJ37Abvs45Rcuxak05T1NHbqK+0n18Sec1vDjz0iAwNyHlRyDnA6hth8RJ7i97r52p07bFqLXpGilkvN0ACKlwkmUR06LnJ9InLtjllIGABkXWzvN2gqrlX6ws+rtOW6vljWmraqrmWmqJY4lLBVjlw0hxwCivn2HOMPOj9cdsdL6gu92t9y0Va0vWyuqqunvND5tfVOTuEwRy25AM7sgHzTwSM9UfP4EvFjtNT4sohKkDyu7rBS6jp3wSUh2ByrZoSpZkqvnJEpQJB9MZYZZu/PoGzDy/cy36e8TdD2huM0yC4aYqrva5DIzCeonrJJJ4nGD+RKYtGcgKu9ecrgj1990/eaapoqHU9Kz0bD8QWCVGNOufUkuT6Ayg8nBx7dCSs7rds75V0mrNQ1uh6TUtCaqG0+ZdIJZKaIr5btHUnA2S7G9QCkA7CpIYmH3Puboe0QXO/WzVel7LeNToiPPR3NLuyNEpUSSLSo+XVWJ2leQAMnHA1FwBcLhLRNmSFBkIBcvqJWp5iQ76SATsRqfkQYeZRExZlTZg1sogdgxKSdncuzuznlFG/EH2Ri0f3mlNongq9L6hrJau01lPIkkTozZaP0cDaxKgY9scnnqMXLtVW0t/paS3QB5LkRTwIoJLyMeSFUEkAckgHgdWx7na37easoaq3W3ViX8PsJjj03USOHTGWQlqRY8n/AHbyDjaR7dD3TWrLlouiuN8012hjub27KS3G5rUYp12k+rEkrovA484An461xwvJXVW6WKoFKgAC4OrGNm374B3hqnybXaraozSlU1ZdJd87YZ++CRlwYtTSXKbTNltlsr7ZcLvUxwRqlNR06lkCx4XG4px9ieeOeih38p7z3N7dRG12G7aaeCh801rtAZI5nWPakRjdiy4WQOSFILJjjJXN6m79d5+6+qdJ22q1StmttwleeWgtEfkI8cLOSjYbfLuEe31seWHVr4+59dpfT405eb2KdJYFNA8wYq7FQfLYkFQxJ4Hs2TxwSbEt0oT0yl02BLLB+YID7dorm604rKeZ4owxeBbDpL6OCK3zll+kQRp5i+oxn1ITn39LDB+Rg/Oel1BdX6m70WS9yLSWG/X1K1RWGvelklabfwCSqbRwBgDjGD89LqazL5S06vCWkuMYST+fOMxf2C4VJM6RPl6FZDrSD7jlBX7Z9qtT2fWlX21bV6w2K20jVNFTrQVFRLQyExLJvhWNZJnZ2BIQiPl3UqvHVdvF/wBvqiwal/GFCzigme31cscJRAQxO4IAVVfMZ8ksSWkHv1ZjxY9wl0NqC3a40xV1NFfa8O1ZT08mVELTMMuqP7biPZvzMR7Y2hi7XN+61guFfqCionp68mDzISzSmT83m4kLYcgj+kexxzz1l3hKf/qO2SrolP8AupGlRY+YJcOCXcHBGY/SGfb5V8oV26UQCEApRjyqBJGejgp6AbRDj4y9ZwNbKGwWejFrtlmgtjJViWQsUC5l2rIEDZXaMg+kn5PDpQeMiWs13NrjWnZ3TN/luFCKT6WMLCgKMWaRi8chYn4HGAPc9fWgO26W3t/qjtZSSUcGp9W1EUdNW16FYvpY2ztDAEq2fccjOD7YPQc7idk+4uihHRXHTFW70MZNZNSt9TEu5vQdycLuHODz1O/EqDKE1JcHsMdoob7OmnXMpKlGgyiSzkFyUAn8g34jeLL3bxIdkNWVVm1VP2lntNrp1ZLvbqaGJBOy7SNjo65UeahBIXODx7Z++53fzwgaj7f320ab7V3envBp2gpJZagMsdQysEcf6htygjlgCBkfcA187baeq9YU50xeLqLJIf5brPF5fnQbYgBgjOcxKSRz0RP/AEpUNVTebDdUMjDKlXBA/Xo6dXLnIQwBYNnDfw9YJsH9P7hc0zaijfQtRIzuAwzgts3o20FHTfiU8HNLaYqO69qL5LLRiClg/nNtZXiJZ8CbO0SGQnOT61xxwOyx+L/w0dvKOPS0nZw1dRQVtUK6WS0007Sq3mbUjeSUNlXZMluCEbGcjIli8KtHFGKi4XuISoBgswXgDA9v0HQk7r9uqy03+pr7XWpdZK6d6ieKijaQQM7FscZwMnjJzx0gqpWiQUpSl3fA5Z/cfrBNx4CullCaysfwwkgjVsTpA3Yk7+kHHS/jb0zpma7PT9kaCVqu4VNTQ1CXBaeSjjmiEezCQerA3EZPBbgjGemq/eMHUmru32p9Batp4aE3xIYrdWRB444oV4JfCvI5IUZbc2c4wOT0LNIeHPu7qi90Onjpia01VzpvrqQ3Q/SrNTjG6VN+C4AIPpyejh3W7a2/VmidC9uIrnRyXzQkctuutdEXMIg3FuC2PkggYBP6Drqm+2z30/g2/aI9OFKnw5KUOSXGSSGfO+zhobvDDpShp6Cl11f/ACJLdDTyo7bTI0VKlQWlcx5BwzCPawyQUYcEjo9QyxayeGti8uuiudShoENH5JkjDb4dsRGBjy0GeOcH+z/4aJNJ6Ehpa+WGkqKShpxHBT1iI0YiI/mKjKfSx25BO8ljjODkDPVHfDTlg7z1mrmt0dD9EadpUp0BSGUiRtgC5BRdhwfkH46se3yUW2UlE0MyRk4BU235Z7ekV9xlxFXTRUUFuDkJKFBOT5gAS2M5ZOXcbRcOw9h+28tmpZtTzaovFxZWSoqLd+IyxLJG7RvEfJXapR0dApJO1VPsQAuhNYPFb2qS3A1ImgnkmmllMF3rqFpWeRm3SojjfJyFLtkkKPYAALpimSripZUFluykj9Yr6nXZ0SkpmSGUAHeVNJfm505zGeWrr9X3GX6e61sk9cry1TVs0xeSUMiFEz+mw4593PTbatQXOy31ZLe53+XG7qTw6iNSQf3Hv0z3qtjMsck0RY+UARnGTzz151VXH9WYVlETPDEN3uTmIDH+D1W1KlFGkIkjSAdhjrGqqO51EmUZ4WQvUnPPZTfT94PFf3nodS3SIXa3/hy08C08Mc3IR8cuGByP0wRgZ+/U/wC3uvrppOer1RS3+KZa4x0+2WQT79vJfb+cDBxgA/HPVYKl7MGanrK6NZg0eNyk4GwAj/569oVo6ZWqIK8GTzFjhdX2lE+fb56NkKEpZKMHOx/TaJcb1Q3pcyku8lK9Ooan0qYEnfc7BuTtFwdV9wdN9wtQ6VrdS2qxNTW+s+qqKqqpv5rRxxPmHy2XefUy4HsSM/HU91D3A0Jqft7fbfp3RdHDUyUc9HAIqeGmn8wxnayezfI5B98dUfj1LqVLjBRnUsrl5hTu0h9KpwAfb2weplWVVRQU0MdXqGjq4Y0cIwpY5QPLi8x/3AHx846kFBMFYShTahncD6xXfEKLTYZv/HXMA2w5bn933i0FJ3g7d26zW2z6i7WJ9QII4ZZquihZdwXDMzcnHuSemPSPdei7b37U8NiodOUNsvlw+oU21hK0QWmQKrQRANjcr44wCxP36qVTa51FV1dQ1ke3I1PUiCHMEccjDBJf+wwM/wDkP16cbxeO4tRE9xuVzqWNWPNYxEbQy5HsM/055/XpObVyUdfYD94IoLbaKyWmdVTZii7N+D5J3DjrFjqXVI7jdwob5UXpPrqKjmpCJp1o6eSNyTlCT5uRtXKlR8joe1+q0kraikFIlZHBK0VPTUtNtiZgcebITy7Ej8zkkfGB0MNMUFuvOq6SwpA9XNUMsZOSzneQTj9j0TO9FTQaRvws+np9gppKSNl80Pty2GXnkDH36OoLhJTUALTgOSRk4H4QbxvOpLJbDbrJKQJqiHW+pQyAztgZ5YLesNmoe7Opm0tcKCO7U1NJE60ZSkVkwrAnc2CQxypXP79Bm7XWrvFFd6p4NrTVdPIVBJwoExxn+x/wOu5r28dvvKoqkfVxkBgCMnzB/wAHpljv0lNbqpWbfUTeXHHlcjyxFLG37gOMdCXO8rrFIExTJZWOX3gPU/WK0t1mTSCbMQnUsqTk7k+Qn259vxjvr+4mq4KG1rR3yojZqV3n4B3SGomOfb/btH7dLpguVKIqG0SKuTPRs7f3+omX/hR0ummbda5BAE1Qwn7x+Ud4dJFot6kk+Cg+ZX3R8x7RH7jLUySep8heBg9OtFYq2/alpLZCDunjgAwcE/yl+fj9+pPcbz26Jlhp9N25xCcCSOqqQspyeQHOcf3A+P16k1J3E0nZWt9ZQaety3WmiHlTB3YoGHAI4UqBgYOcZPTNLUFA6sbRMJVNLVSrBmgF0kYPft3iN6k7U38TC409TSzRt6WUzBGjC8c7sY9uoW61NARHMVdopslQ+QcfqD0WtQ9z9NXiH6K8aXpvOji5lE0qkueSdmSuef8APTZJeO2wo5IX0dHI5ZWZ5J5Imzj2A/p/bA+elVqQVEpMKCmQuqmq8dIBJIcK6v8AKYHv17CbMzv6n3ZHPHROvei6+06SgvEFdXTuQ1XIhoGjVPqUCFM5I27Ubn9cY468aus7PzbVptKT0s0Ue0sa551Zgvqx7jBJ444+/U5o9f8Abmv06lpu1jmqqWjpjHGgqmibBZ342Fc4LN7ew4+3RtCoKUtBmBLjcvu/YQw36mVJUiYlpuchHQgj72nrAAjp6oXWimggk8wHfJtyct5jHkD2+Bg9Pa6H1x+HivCz04jjbdHKZEZgCQcA+5B4IHt0SIq7sfJf5rxarNdqeOaQ4gluL4QYHu3qZgfds4Gfbj2sEtfV2WzRXaO6TUFoqqfZUQz05eCSIADMUkq4VvUF3DaPkE56SmoS5AUD6P8AsINp6ebNo0qCkpLnyqd8t0BHLq/aKg6U11qHthr2j1tp6sSnuNCkbwsyq/PlKDwwI/z12au7nX/uVqC8az1PXedX1E1K3rCKx2uc4CgDj9B0SlsfZO93lmnspYyO52itmAKheOd32+cf3646ixdqNO3WOCv0XPUwCRWXfdGAUH8uTwoBPPq9x0tTIKpuoLSBnd+YPQGF+KrYaZRqA0zUX8hBPxOxCilvZ4D89SZLDdHDHmpp2H7mXphNRIYiNx9ujfe7x2dgpauiGjp089knYJM/qwGK7cOQByfbjqEQ1Xa8zh2prn5W4M0bSKFA+2Rz0tXUSE6Ameg4PM/MTzHeInb6+avxCunmIyDkJz5Ujko9Ij1yqlNrsYAbK0Dg4+/1U/S6KP452empaWOXS8UawRFI1aqLYUuzn1F8n1M3PP2+Ol0Uu1SZjK+0o2HzdB/jAUq81EoFP2OZ8Svk5qJ+eAHkiYxg8B8e3T9bqalnVpqmmWVl2fmZgCAntwR0ul1GURMU/AfUfrDdeKvN1qTDBFAm7CxpuIUY9gWJb/J684XLqAccuPjpdLrw/FHQzMPvHoGZVCBjjeT/AMdOFLcq+mt1RT09XLFFUhopkVyBInpbaR9tyqf7qPt0ul10nc+n7RxN3H85Rzx1NRDU0pSTPme4ZQw98exHT/qfW+p7/Pb7ldLhE0r0YXbDRwQRgB2Ufy4kVM4UZYgsT7k9LpdfLJAYR6k+SOOk1Zf7PdHr7dXLFNFHkEwRurcD8yspDfuD17XnXurdYz1V01HeHq55XhDehETCnAARQFAwPYDHS6XSks+dvX6R5XEufX9YZ5ZZZo5zJISWYE8/bPTczOnKyMMYI5+el0uuV8v5zMIJ/n5R0zuxgpMn/wBn/wC7dLpdLpSZv7D6QnL29z9TH//Z"
    )
