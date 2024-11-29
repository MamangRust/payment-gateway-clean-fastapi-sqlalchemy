from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from domain.dtos.record.claims import Claims
from core.errors import TokenGenerationError, TokenExpiredError, TokenValidationError

class JwtConfig:
    def __init__(self, jwt_secret: str, jwt_expired: int):
        self.jwt_secret = jwt_secret
        self.jwt_token_expiration_minutes = jwt_expired

    def generate_token(self, user_id: int) -> str:
        """
        Generates a JWT token for a given user ID.

        :param user_id: ID of the user
        :return: Encoded JWT token
        :raises TokenGenerationError: If token generation fails
        """
        try:
            # Set the expiration time based on the provided expiration duration
            exp_time = datetime.utcnow() + timedelta(minutes=self.jwt_token_expiration_minutes)
            claims = Claims(
                user_id=user_id, 
                exp=exp_time.timestamp(),  # Set the expiration as a Unix timestamp
                iat=datetime.utcnow().timestamp()
            )
            # Encode the token
            token = jwt.encode(claims.dict(), self.jwt_secret, algorithm="HS256")
           
            return token
        except Exception as e:
            raise TokenGenerationError(f"Failed to generate token: {str(e)}")

    def verify_token(self, token: str) -> Optional[int]:
        try:
            # Decode the token and verify its signature and claims
            decoded_token = jwt.decode(token, self.jwt_secret, algorithms="HS256")
            claims = Claims(**decoded_token)

            # Use UTC time for comparison
            current_time = datetime.utcnow().timestamp()
            
            # Check if the current time is before the expiration time
            if claims.exp > current_time:
                return claims.user_id
            else:
                raise TokenExpiredError("Token has expired")
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.JWTError as e:
            raise TokenValidationError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise TokenValidationError(f"Token validation failed: {str(e)}")
