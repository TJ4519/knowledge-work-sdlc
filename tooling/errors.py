class SDLCError(RuntimeError):
    """Base error for rejected author-tool operations."""


class IntegrityError(SDLCError):
    """A source, package, or installation integrity relation failed."""
