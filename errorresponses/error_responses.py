from fastapi import HTTPException, status

authorization_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could Not Validate Token",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could Not Validate Token",
    headers={"WWW-Authenticate": "Bearer"},
)

authentication_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

no_data_exception = HTTPException(
    status_code=status.HTTP_200_OK,
    detail=""
)