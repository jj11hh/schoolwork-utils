Private Sub Command1_Click
    Dim I As Integer
    For I = 0 To 100
        Print Str(I)
        If I Mod 5 = 0 Then
            Print "I mod 5 = 0"
        End If
        If I Mod 3 = 0 Then Print "I mod 3 = 0"
    Next I
End Sub
